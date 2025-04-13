import yaml


def load_video_plan_yaml(path="src/plans/video_plan_001.yml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
