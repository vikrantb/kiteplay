from dagster import AssetIn, asset, AssetExecutionContext


def create_dagster_assets_from_graph(ordered_assets):
    dagster_assets = []
    def create_dagster_asset(asset_obj):
        asset_id = asset_obj.id
        deps = {dep: AssetIn() for dep in asset_obj.get_dependencies()}

        @asset(name=asset_id, ins=deps)
        def dagster_asset(context: AssetExecutionContext, **kwargs) -> str:
            requirements = {
                "id": asset_id,
                "description": getattr(asset_obj, "description", None),
                "creation_strategy": getattr(asset_obj, "creation_strategy", None),
                "text": getattr(asset_obj, "text", None),
            }
            config = asset_obj.get_config()
            context.log.info(f"Preparing to generate {asset_id} with requirements: {requirements} and config: {config}")
            asset_obj.set_context(requirements=requirements, config=config)
            result = asset_obj.generate()
            return result

        return dagster_asset

    # Create Dagster assets for each asset in the ordered list
    for asset_obj in ordered_assets:
        dagster_assets.append(create_dagster_asset(asset_obj))
    return dagster_assets
