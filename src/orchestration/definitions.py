from dagster import Definitions, asset, AssetExecutionContext

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

def build_and_get_scene_assets():
    for scene in plan.get("scenes", []):
        scene_id = scene["id"]
        background = scene["background"]
        voiceover = scene.get("voiceover", scene.get("text", ""))

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
    # Placeholder for future voiceover/audio asset generation
    # Could be driven by narration script, character dialogue, etc.
    pass

def build_and_get_video_assets():
    for video in plan.get("videos", []):
        video_id = video["id"]
        scene_sequence = video["sequence"]
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
