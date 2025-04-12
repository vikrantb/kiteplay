import yaml
from pathlib import Path


def load_video_plan_yaml(path: str = "plans/video_plan_001.yml") -> dict:
    plan_path = Path(path)
    if not plan_path.exists():
        raise FileNotFoundError(f"Video plan not found: {plan_path}")
    with open(plan_path, "r") as f:
        return yaml.safe_load(f)