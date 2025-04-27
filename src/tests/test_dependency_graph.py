from data_models.Video import Video
from orchestration.dependency_graph import get_ordered_assets_from_plan
from utils.yaml_loader import load_video_plan_yaml


def test_get_ordered_assets_from_plan():
    # Mock the plan with a video and voiceover
    plan = load_video_plan_yaml()
    ordered_assets = get_ordered_assets_from_plan(plan)
    assert ordered_assets == ["video1", "vo1"], f"Expected ['video1', 'vo1'], but got {ordered_assets}"
    assert True
