from collections import defaultdict, deque
from pprint import pprint

from data_models.Image import Image
from data_models.Scene import Scene
from data_models.Video import Video
from data_models.Voiceover import Voiceover
import logging


def load_all_assets(plan):
    """
    Load all asset objects from the plan and return a dictionary of id -> asset.
    """
    assets = {}
    for asset in (
        Image.load_from_plan(plan)
        + Scene.load_from_plan(plan)
        + Video.load_from_plan(plan)
        + Voiceover.load_from_plan(plan)
    ):
        assets[asset.id] = asset
    return assets


def build_dependency_graph(assets):
    """
    Construct the DAG from asset dependencies and compute in-degrees for topological sorting.
    """
    graph = defaultdict(set)
    in_degree = defaultdict(int)

    for asset in assets.values():
        for dep in set(asset.get_dependencies()):
            if dep not in assets:
                raise ValueError(
                    f"{asset.__class__.__name__} '{asset.id}' references missing dependency '{dep}'"
                )
            graph[dep].add(asset.id)
            in_degree[asset.id] += 1
        graph.setdefault(asset.id, set())

    return graph, in_degree


def perform_topological_sort_using_kahns(graph, in_degree, all_ids):
    """
    Perform Kahn's algorithm to detect cycles and produce a topologically sorted list.
    Logs full graph and unresolved dependencies on failure.
    """
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
        logging.error("Cycle detected or missing dependencies. Full graph:")
        logging.error(pprint(graph))
        logging.error("Unresolved nodes with in-degree:")
        for node, degree in in_degree.items():
            if degree > 0:
                logging.error(f"{node}: {degree}")
        raise ValueError("Cycle detected or unresolved dependencies exist.")

    return sorted_order


def get_ordered_assets_from_plan(plan):
    """
    Load, validate, and return assets in topologically sorted order.
    """
    assets = load_all_assets(plan)
    graph, in_degree = build_dependency_graph(assets)
    sorted_ids = perform_topological_sort_using_kahns(graph, in_degree, assets.keys())
    for asset in assets.values():
        asset.validate(set(assets.keys()))
    return [assets[i] for i in sorted_ids]