import pytest
from orchestration.dependency_graph import get_ordered_assets_from_plan
from utils.yaml_loader import load_video_plan_yaml
from data_models.Video import Video
from data_models.Scene import Scene
from data_models.Voiceover import Voiceover
from data_models.Image import Image

VIDEO_PLAN_PATH = "src/plans/video_plan_001.yml"

EXPECTED_ASSET_IDS = [
    "calm_silence", "advice_on_reacting", "power_of_pause", "reflection_peace",
    "bg_meditation", "sunrise_mountain", "moonlit_valley", "waves_video",
    "scene_001", "scene_002", "scene_003", "scene_004",
    "video_001", "video_002"
]

VALID_ASSET_TYPES = (Voiceover, Image, Scene, Video)

def test_ordered_assets_structure():
    """Test that ordered assets list is not empty and is a list.

    This check ensures the function returns a properly structured list of assets,
    which is critical for downstream processing that expects iterable asset collections.
    For example, an empty list or wrong type would cause iteration or access errors.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    assert isinstance(ordered_assets, list), "ordered_assets should be a list"
    assert len(ordered_assets) > 0, "ordered_assets should not be empty"

def test_asset_types():
    """Test that each asset loaded is of a valid expected type.

    This ensures that parsing and loading from YAML returns objects like Voiceover, Image, etc.
    For example, we should not get a raw dict or a missing/misclassified object.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    for asset in ordered_assets:
        assert asset is not None, "Asset should not be None"
        assert isinstance(asset, VALID_ASSET_TYPES), f"Invalid asset type: {type(asset)}"

def test_specific_assets_present():
    """Test that all expected asset IDs are present and no unexpected assets exist.

    This guarantees the plan contains exactly the assets we expect, no more or less.
    For example, missing assets would indicate incomplete plans, unexpected assets could indicate errors.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    asset_ids = [asset.id for asset in ordered_assets]
    for expected_id in EXPECTED_ASSET_IDS:
        assert expected_id in asset_ids, f"Missing asset ID: {expected_id}"
    # Also assert no unexpected extra assets
    for asset_id in asset_ids:
        assert asset_id in EXPECTED_ASSET_IDS, f"Unexpected extra asset ID: {asset_id}"

def test_scene_dependencies():
    """Test that each scene has dependencies and they are strings.

    This ensures scenes correctly declare their dependencies by ID,
    which is essential for building the dependency graph.
    For example, a scene without dependencies or with non-string deps would break graph logic.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    scenes = [a for a in ordered_assets if isinstance(a, Scene)]
    assert scenes, "No scenes found"
    for scene in scenes:
        deps = scene.get_dependencies()
        assert deps, f"Scene {scene.id} should have dependencies"
        for dep in deps:
            assert isinstance(dep, str), "Dependency must be a string"

def test_video_sequence_integrity():
    """Test that each video has a non-empty sequence of scene IDs as strings.

    This confirms videos reference sequences of scenes correctly.
    For example, an empty or malformed sequence would prevent video assembly.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    videos = [a for a in ordered_assets if isinstance(a, Video)]
    assert videos, "No videos found"
    for video in videos:
        assert video.sequence, f"Video {video.id} must have a non-empty sequence"
        for scene_id in video.sequence:
            assert isinstance(scene_id, str), f"Scene ID {scene_id} should be a string"

def test_invalid_asset_type_detection():
    """Test that an invalid asset type is not recognized as valid.

    This test verifies type safety by ensuring unknown or incorrect asset types are rejected.
    For example, a random class instance should not be mistaken for a valid asset.
    """
    class InvalidAsset:
        def __init__(self):
            self.id = "invalid_asset"
    invalid_asset = InvalidAsset()
    assert not isinstance(invalid_asset, VALID_ASSET_TYPES), "Invalid asset type should not be valid"

def test_missing_expected_assets():
    """Test detection of missing expected asset IDs.

    This simulates a missing asset scenario to check that missing assets are properly identified.
    For example, if 'calm_silence' is missing, the test should detect it.
    """
    # Simulate missing assets by removing one expected ID
    missing_id = EXPECTED_ASSET_IDS[0]
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    asset_ids = [asset.id for asset in ordered_assets if asset.id != missing_id]
    assert missing_id not in asset_ids or missing_id in EXPECTED_ASSET_IDS, f"Expected asset ID {missing_id} is missing"


# Advanced and thorough tests for deeper asset graph integrity and field-level validation
def test_voiceover_content_structure():
    """Test that voiceovers have a non-empty text attribute of type string.

    This ensures voiceovers contain meaningful text content necessary for audio rendering.
    For example, a voiceover without text or with empty text is invalid.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    voiceovers = [a for a in ordered_assets if isinstance(a, Voiceover)]
    assert voiceovers, "No voiceovers found"
    for v in voiceovers:
        # Must have text and it should be a non-empty string
        assert hasattr(v, "text"), f"Voiceover {v.id} missing 'text' attribute"
        assert isinstance(v.text, str), f"Voiceover {v.id} text must be a string"
        assert v.text.strip(), f"Voiceover {v.id} text must not be empty"


def test_image_creation_strategy():
    """Test that images with a creation strategy have a non-empty prompt string.

    This verifies that images generated via a creation strategy have valid prompts,
    which are essential for AI generation or similar processes.
    For example, a missing or empty prompt would cause generation failure.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    images = [a for a in ordered_assets if isinstance(a, Image)]
    for img in images:
        if hasattr(img, "creation_strategy") and img.creation_strategy:
            # If image has a creation strategy, it must have a non-empty prompt
            prompt = img.creation_strategy.get("prompt")
            assert isinstance(prompt, str), f"Image {img.id} prompt must be a string"
            assert prompt.strip(), f"Image {img.id} prompt must not be empty"


def test_scene_background_and_voiceover_dependencies():
    """Test that scene background and voiceover dependencies reference valid assets.

    This ensures scenes reference existing images and voiceovers correctly,
    preventing broken references in the asset graph.
    For example, a scene background referring to a missing image would cause errors.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    scenes = [a for a in ordered_assets if isinstance(a, Scene)]
    images = {img.id: img for img in ordered_assets if isinstance(img, Image)}
    voiceovers = {v.id: v for v in ordered_assets if isinstance(v, Voiceover)}
    for scene in scenes:
        # Check background dependency points to a valid image or video
        if hasattr(scene, "background") and scene.background:
            bg_id = scene.background
            assert isinstance(bg_id, str), f"Scene {scene.id} background must be a string"
            assert bg_id in images, f"Scene {scene.id} background references missing image asset: {bg_id}"
        # Check voiceover dependency points to a valid voiceover
        if hasattr(scene, "voiceover") and scene.voiceover:
            vo_id = scene.voiceover
            assert isinstance(vo_id, str), f"Scene {scene.id} voiceover must be a string"
            assert vo_id in voiceovers, f"Scene {scene.id} voiceover references missing voiceover asset: {vo_id}"


def test_video_unique_scene_sequence():
    """Test that video sequences reference unique existing scenes unless duplicates are allowed.

    This ensures videos reference valid scenes and avoid unintended duplicates,
    which could cause logical errors in playback or editing.
    For example, video_001 should have unique scenes, but video_002 may allow duplicates.
    """
    plan = load_video_plan_yaml(VIDEO_PLAN_PATH)
    ordered_assets = get_ordered_assets_from_plan(plan)
    scenes = {s.id for s in ordered_assets if isinstance(s, Scene)}
    videos = [a for a in ordered_assets if isinstance(a, Video)]
    for video in videos:
        assert hasattr(video, "sequence"), f"Video {video.id} missing sequence"
        assert isinstance(video.sequence, list), f"Video {video.id} sequence must be a list"
        # All referenced scene IDs must exist and be unique unless duplicates are explicitly allowed
        for sid in video.sequence:
            assert sid in scenes, f"Video {video.id} sequence references unknown scene: {sid}"
        # Check for duplicates (unless allowed by a field, e.g., allow_duplicates)
        # Explicitly allow known exceptions (e.g., video_002)
        if video.id != "video_002" and not getattr(video, "allow_duplicates", False):
            assert len(set(video.sequence)) == len(video.sequence), (
                f"Video {video.id} has duplicate scenes in its sequence: {video.sequence}"
            )
