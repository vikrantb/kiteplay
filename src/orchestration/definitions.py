from dagster import Definitions
from orchestration.dependency_graph import get_ordered_assets_from_plan
from utils.dagster_assets_helper import create_dagster_assets_from_graph
from utils.yaml_loader import load_video_plan_yaml

plan = load_video_plan_yaml()
ordered_assets = get_ordered_assets_from_plan(plan)
dagster_assets = []

create_dagster_assets_from_graph()

defs = Definitions(assets=dagster_assets)
