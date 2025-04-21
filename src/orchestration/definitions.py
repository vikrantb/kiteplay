from dagster import Definitions, asset, AssetExecutionContext
from orchestration.dependency_graph import get_ordered_assets_from_plan
from utils.plan_loading import load_video_plan_yaml

plan = load_video_plan_yaml()
ordered_assets = get_ordered_assets_from_plan(plan)

dagster_assets = []

for asset_obj in ordered_assets:
    asset_id = asset_obj.id

    @asset(name=f"generate_{asset_id}")
    def dagster_asset(context: AssetExecutionContext, asset_id=asset_id) -> str:
        context.log.info(f"Generating asset {asset_id}")
        return f"{asset_id}.generated"

    dagster_assets.append(dagster_asset)

defs = Definitions(assets=dagster_assets)
