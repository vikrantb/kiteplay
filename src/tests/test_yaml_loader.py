"""
Unit tests for validating the structure and content of a video plan YAML file.

This test suite ensures:
- The video plan YAML can be successfully loaded from disk.
- The loaded plan contains valid 'scenes' and 'videos' structure.
- Each scene has the required fields and format.
- Each video references valid scene IDs in the correct order.
"""

from utils.yaml_loader import load_video_plan_yaml
from pathlib import Path


def test_scene(scene):
    assert isinstance(scene, dict)
    assert "id" in scene
    test_background(scene)
    test_scene_audio(scene)


def test_scene_audio(scene):
    assert "voiceover" in scene or "text" in scene or "music" in scene


def test_background(scene):
    assert "background" in scene
    assert "background_type" in scene


def test_scenes(plan, scenes):
    if "scenes" in plan:
        for scene in plan["scenes"]:
            test_scene(scene)
            scenes[scene["id"]] = scene


def test_video(scenes, video):
    assert isinstance(video, dict)
    assert "id" in video
    assert "sequence" in video
    assert isinstance(video["sequence"], list)
    for scene_id in video["sequence"]:
        assert scene_id in scenes


def test_videos(plan, scenes):
    for video in plan["videos"]:
        test_video(scenes, video)


# Test loading a video plan YAML file
def test_load_video_plan_yaml():
    # Test loading a valid YAML file
    plan = load_video_plan_yaml("test_plans/video_plan_001.yml")
    assert isinstance(plan, dict)
    scenes = {}
    test_scenes(plan, scenes)

    assert "videos" in plan
    test_videos(plan, scenes)

    # Test loading a non-existent file
    try:
        load_video_plan_yaml("non_existent_file.yml")
    except FileNotFoundError as e:
        assert str(e) == "Video plan not found: non_existent_file.yml"
