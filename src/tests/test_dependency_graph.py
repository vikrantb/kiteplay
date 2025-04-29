import pytest
from orchestration.dependency_graph import get_ordered_assets_from_plan
from utils.yaml_loader import load_video_plan_yaml
from data_models.Video import Video
from data_models.Scene import Scene
from data_models.Voiceover import Voiceover
from data_models.Image import Image


def test_ordered_assets_structure():
    plan = load_video_plan_yaml("src/plans/video_plan_001.yml")
    ordered_assets = get_ordered_assets_from_plan(plan)
    assert isinstance(ordered_assets, list), "ordered_assets should be a list"
    assert len(ordered_assets) > 0, "ordered_assets should not be empty"

def test_asset_types():
    plan = load_video_plan_yaml("src/plans/video_plan_001.yml")
    ordered_assets = get_ordered_assets_from_plan(plan)
    valid_types = (Voiceover, Image, Scene, Video)
    for asset in ordered_assets:
        assert isinstance(asset, valid_types), f"Invalid asset type: {type(asset)}"

def test_specific_assets_present():
    plan = load_video_plan_yaml("src/plans/video_plan_001.yml")
    ordered_assets = get_ordered_assets_from_plan(plan)
    asset_ids = [asset.id for asset in ordered_assets]
    expected_ids = [
        "calm_silence", "advice_on_reacting", "power_of_pause", "reflection_peace",
        "bg_meditation", "sunrise_mountain", "moonlit_valley", "waves_video",
        "scene_001", "scene_002", "scene_003", "scene_004",
        "video_001", "video_002"
    ]
    for expected_id in expected_ids:
        assert expected_id in asset_ids, f"Missing asset ID: {expected_id}"

def test_scene_dependencies():
    plan = load_video_plan_yaml("src/plans/video_plan_001.yml")
    ordered_assets = get_ordered_assets_from_plan(plan)
    scenes = [a for a in ordered_assets if isinstance(a, Scene)]
    assert scenes, "No scenes found"
    for scene in scenes:
        deps = scene.get_dependencies()
        assert deps, f"Scene {scene.id} should have dependencies"
        for dep in deps:
            assert isinstance(dep, str), "Dependency must be a string"

def test_video_sequence_integrity():
    plan = load_video_plan_yaml("src/plans/video_plan_001.yml")
    ordered_assets = get_ordered_assets_from_plan(plan)
    videos = [a for a in ordered_assets if isinstance(a, Video)]
    assert videos, "No videos found"
    for video in videos:
        assert video.sequence, f"Video {video.id} must have a non-empty sequence"
        for scene_id in video.sequence:
            assert isinstance(scene_id, str), f"Scene ID {scene_id} should be a string"
