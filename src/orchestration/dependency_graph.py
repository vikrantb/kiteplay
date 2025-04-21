from collections import defaultdict, deque
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
        for dep in asset.dependencies():
            if dep not in assets:
                raise ValueError(
                    f"{asset.__class__.__name__} '{asset.id}' references missing dependency '{dep}'"
                )
            graph[dep].add(asset.id)
            in_degree[asset.id] += 1
        graph.setdefault(asset.id, set())

    return graph, in_degree


def perform_topological_sort(graph, in_degree, all_ids):
    """
    Perform Kahn's algorithm to detect cycles and produce a topologically sorted list.
    Logs full graph and unresolved dependencies on failure.
    """
    logging.debug("==== Dependency Graph Structure ====")
    for node in sorted(graph):
        logging.debug(f"{node} -> {sorted(graph[node])}")
    logging.debug("==== In-degree Table ====")
    for node in sorted(all_ids):
        logging.debug(f"{node}: in-degree = {in_degree[node]}")

    queue = deque([node for node in all_ids if in_degree[node] == 0])
    logging.debug(f"Initial nodes with zero in-degree: {list(queue)}")
    sorted_order = []

    while queue:
        node = queue.popleft()
        logging.debug(f"Processing node: {node}")
        sorted_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            logging.debug(f"Decremented in-degree of neighbor {neighbor} to {in_degree[neighbor]}")
            if in_degree[neighbor] == 0:
                logging.debug(f"Neighbor {neighbor} now has zero in-degree, adding to queue")
                queue.append(neighbor)

    if len(sorted_order) != len(all_ids):
        unresolved = [node for node in all_ids if node not in sorted_order]
        incoming_edges = {node: [] for node in unresolved}
        for src, dsts in graph.items():
            for node in unresolved:
                if node in dsts:
                    incoming_edges[node].append(src)
        logging.error("Cycle detected in dependency graph.")
        logging.error(f"Unresolved nodes: {unresolved}")
        logging.error(f"Incoming edge map for unresolved nodes: {incoming_edges}")
        raise ValueError("Cycle detected in dependency graph. Check logs for details.")
    return sorted_order


def get_ordered_assets_from_plan(plan):
    """
    Load, validate, and return assets in topologically sorted order.
    """
    assets = load_all_assets(plan)
    graph, in_degree = build_dependency_graph(assets)
    sorted_ids = perform_topological_sort(graph, in_degree, assets.keys())
    for asset in assets.values():
        asset.validate(set(assets.keys()))
    return [assets[i] for i in sorted_ids]