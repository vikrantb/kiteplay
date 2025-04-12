from dagster import asset, AssetExecutionContext
from utils.yaml_loader import load_video_plan_yaml


@asset
def load_video_plan(context: AssetExecutionContext) -> dict:
    plan = load_video_plan_yaml()
    context.log.info(f"Loaded video plan with {len(plan['video'])} scenes")
    return plan

@asset
def generate_scene_visuals(load_video_plan: dict) -> list:
    visuals = []
    for scene in load_video_plan['scenes']:
        bg = scene['background']
        visuals.append(f"generated_visual_for_{bg}")
    return visuals

@asset
def generate_scene_voiceovers(load_video_plan: dict) -> list:
    voiceovers = []
    for scene in load_video_plan['scenes']:
        vo = scene.get("voiceover", scene.get("text"))
        voiceovers.append(f"tts_audio_for_{vo}")
    return voiceovers

@asset
def compose_videos(load_video_plan: dict,
                   generate_scene_visuals: list,
                   generate_scene_voiceovers: list) -> list:
    outputs = []
    for video in load_video_plan['videos']:
        scene_ids = video['sequence']
        outputs.append(f"composed_video_{video['id']}")
    return outputs