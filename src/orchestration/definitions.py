from dagster import Definitions, asset, AssetExecutionContext
from collections import defaultdict

from orchestration.dependency_graph import get_dependency_graph
from utils.plan_loading import load_video_plan_yaml

plan = load_video_plan_yaml()
dependency_graph = get_dependency_graph(plan)

scene_assets = []
scene_id_to_asset = {}
voiceover_assets = []

image_assets = []
image_id_to_asset = {}

video_assets = []

def collect_all_asset_ids(plan):
    asset_ids = set()
    for section in ["images", "voiceovers", "scenes", "videos"]:
        for item in plan.get(section, []):
            asset_ids.add(item["id"])
    return asset_ids

def add_voiceover_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for scene in plan.get("scenes", []):
        scene_id = scene["id"]
        voiceover_id = scene.get("voiceover_id")
        if voiceover_id:
            if voiceover_id not in all_ids:
                raise ValueError(f"Scene '{scene_id}' references missing voiceover_id '{voiceover_id}'")
            graph[voiceover_id].add(scene_id)
            in_degree[scene_id] += 1
        graph.setdefault(scene_id, set())

def add_video_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for video in plan.get("videos", []):
        video_id = video["id"]
        sequence = video.get("sequence")
        if not sequence:
            graph.setdefault(video_id, set())
            continue
        for scene_id in sequence:
            if scene_id not in all_ids:
                raise ValueError(f"Video '{video_id}' references missing scene '{scene_id}'")
            graph[scene_id].add(video_id)
            in_degree[video_id] += 1
        graph.setdefault(video_id, set())

def add_scene_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for scene in plan.get("scenes", []):
        scene_id = scene["id"]
        bg_id = scene.get("background")
        if bg_id:
            if bg_id not in all_ids:
                raise ValueError(f"Scene '{scene_id}' references missing background '{bg_id}'")
            graph[bg_id].add(scene_id)
            in_degree[scene_id] += 1
        graph.setdefault(scene_id, set())

def build_and_get_scene_assets():
    for scene in plan.get("scenes", []):
        scene_id = scene["id"]
        background = scene["background"]
        voiceover = scene.get("voiceover", scene.get("text", ""))

        # Validate voiceover_id if present
        voiceover_id = scene.get("voiceover_id")
        if voiceover_id and voiceover_id not in voiceover_assets:
            raise ValueError(f"Scene '{scene_id}' references missing voiceover_id '{voiceover_id}'")

        @asset(name=f"generate_scene_{scene_id}")
        def scene_asset(context: AssetExecutionContext, scene_id=scene_id, background=background,
                        voiceover=voiceover) -> str:
            context.log.info(f"Generating scene {scene_id} with background {background} and voiceover {voiceover}")
            return f"scene_{scene_id}.mp4"

        scene_assets.append(scene_asset)
        scene_id_to_asset[scene_id] = scene_asset

def build_and_get_image_assets():
    for image in plan.get("images", []):
        image_id = image["id"]
        description = image.get("description", "")

        @asset(name=f"generate_image_{image_id}")
        def image_asset(context: AssetExecutionContext, image_id=image_id, description=description) -> str:
            context.log.info(f"Generating image {image_id} with description '{description}'")
            return f"image_{image_id}.png"

        image_assets.append(image_asset)
        image_id_to_asset[image_id] = image_asset

def build_and_get_voiceover_assets():
    for voiceover in plan.get("voiceovers", []):
        voiceover_id = voiceover["id"]
        text = voiceover["text"]

        @asset(name=f"generate_voiceover_{voiceover_id}")
        def voiceover_asset(context: AssetExecutionContext, voiceover_id=voiceover_id, text=text) -> str:
            context.log.info(f"Generating voiceover {voiceover_id} with text '{text}'")
            return f"voiceover_{voiceover_id}.mp3"

        voiceover_assets.append(voiceover_asset)

def build_and_get_video_assets():
    for video in plan.get("videos", []):
        video_id = video["id"]
        scene_sequence = video.get("sequence")
        if not scene_sequence:
            continue
        input_assets = [scene_id_to_asset[sid] for sid in scene_sequence]

        @asset(name=f"generate_video_{video_id}", deps=input_assets)
        def video_asset(context: AssetExecutionContext, **scene_outputs) -> str:
            ordered_scenes = [scene_outputs[f"generate_scene_{sid}"] for sid in scene_sequence]
            context.log.info(f"Composing video {video_id} from scenes {scene_sequence}")
            return f"video_{video_id}.mp4"

        video_assets.append(video_asset)

build_and_get_image_assets()
build_and_get_scene_assets()
build_and_get_voiceover_assets()
build_and_get_video_assets()

defs = Definitions(assets=image_assets + scene_assets + voiceover_assets + video_assets)
