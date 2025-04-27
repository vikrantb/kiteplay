from dagster import Definitions, asset, AssetExecutionContext
from orchestration.dependency_graph import get_ordered_assets_from_plan
from utils.yaml_loader import load_video_plan_yaml

plan = load_video_plan_yaml()
ordered_assets = get_ordered_assets_from_plan(plan)

dagster_assets = []

# Create a Dagster asset for each asset in the ordered list
from dagster import asset, AssetExecutionContext, AssetIn

def create_dagster_asset(asset_obj):
    asset_id = asset_obj.id
    deps = {}

    # Detect dependencies based on asset type
    if hasattr(asset_obj, "background") and hasattr(asset_obj, "voiceover"):
        # It's a scene
        deps[asset_obj.background] = AssetIn()
        deps[asset_obj.voiceover] = AssetIn()

    elif hasattr(asset_obj, "sequence"):
        # It's a video
        for scene_id in set(asset_obj.sequence):
            deps[scene_id] = AssetIn()

    else:
        # It's a voiceover or image (no dependencies)
        deps = {}

    @asset(name=asset_id, ins=deps)
    def dagster_asset(context: AssetExecutionContext, **kwargs) -> str:
        context.log.info(f"Generating asset {asset_id} with dependencies {list(kwargs.keys())}")
        return f"{asset_id}.generated"

    return dagster_asset

# Create Dagster assets for each asset in the ordered list
for asset_obj in ordered_assets:
    dagster_assets.append(create_dagster_asset(asset_obj))

defs = Definitions(assets=dagster_assets)
