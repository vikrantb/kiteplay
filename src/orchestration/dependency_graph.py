from collections import defaultdict, deque
from data_models.Image import Image
from data_models.Scene import Scene
from data_models.Video import Video


def load_all_assets(plan):
    assets = {}
    for asset in Image.load_from_plan(plan) + Scene.load_from_plan(plan) + Video.load_from_plan(plan):
        assets[asset.id] = asset
    return assets


def build_dependency_graph(assets):
    graph = defaultdict(set)
    in_degree = defaultdict(int)

    for asset in assets.values():
        for dep in asset.dependencies():
            if dep not in assets:
                raise ValueError(f"{asset.__class__.__name__} '{asset.id}' references missing dependency '{dep}'")
            graph[dep].add(asset.id)
            in_degree[asset.id] += 1
        graph.setdefault(asset.id, set())

    return graph, in_degree


def perform_topological_sort(graph, in_degree, all_ids):
    queue = deque([node for node in all_ids if in_degree[node] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(all_ids):
        raise ValueError("Cycle detected in dependency graph.")
    return sorted_order


def get_ordered_assets_from_plan(plan):
    assets = load_all_assets(plan)
    graph, in_degree = build_dependency_graph(assets)
    sorted_ids = perform_topological_sort(graph, in_degree, assets.keys())
    for asset in assets.values():
        asset.validate(set(assets.keys()))
    return [assets[i] for i in sorted_ids]
