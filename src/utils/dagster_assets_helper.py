from dagster import AssetIn, asset, AssetExecutionContext

from orchestration.definitions import ordered_assets, dagster_assets


def create_dagster_assets_from_graph():
    def create_dagster_asset(asset_obj):
        asset_id = asset_obj.id
        deps = {dep: AssetIn() for dep in asset_obj.get_dependencies()}

        @asset(name=asset_id, ins=deps)
        def dagster_asset(context: AssetExecutionContext, **kwargs) -> str:
            context.log.info(f"Generating asset {asset_id} with dependencies {list(kwargs.keys())}")
            return f"{asset_id}.generated"

        return dagster_asset

    # Create Dagster assets for each asset in the ordered list
    for asset_obj in ordered_assets:
        dagster_assets.append(create_dagster_asset(asset_obj))
