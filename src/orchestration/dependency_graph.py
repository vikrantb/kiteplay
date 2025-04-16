from collections import deque, defaultdict


def collect_all_asset_ids(plan):
    asset_ids = set()
    for section in ["images", "voiceovers", "scenes", "videos"]:
        for item in plan.get(section, []):
            asset_ids.add(item["id"])
    return asset_ids


def add_voiceover_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for scene in plan.get("scenes", []):
        scene_id = scene["id"]
        voiceover_id = scene.get("voiceover_id")
        if voiceover_id:
            if voiceover_id not in all_ids:
                raise ValueError(f"Scene '{scene_id}' references missing voiceover_id '{voiceover_id}'")
            graph[voiceover_id].add(scene_id)
            in_degree[scene_id] += 1
        graph.setdefault(scene_id, set())


def add_video_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for video in plan.get("videos", []):
        video_id = video["id"]
        sequence = video.get("sequence")
        if not sequence:
            graph.setdefault(video_id, set())
            continue
        for scene_id in sequence:
            if scene_id not in all_ids:
                raise ValueError(f"Video '{video_id}' references missing scene '{scene_id}'")
            graph[scene_id].add(video_id)
            in_degree[video_id] += 1
        graph.setdefault(video_id, set())


def add_image_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for image in plan.get("images", []):
        image_id = image["id"]
        bg_id = image.get("background")  # optional for gif creation from video/image
        if bg_id:
            if bg_id not in all_ids:
                raise ValueError(f"Image '{image_id}' references missing background '{bg_id}'")
            graph[bg_id].add(image_id)
            in_degree[image_id] += 1
        graph.setdefault(image_id, set())


def add_scene_dependencies_to_graph(plan, graph, in_degree, all_ids):
    for scene in plan.get("scenes", []):
        scene_id = scene["id"]
        bg_id = scene.get("background")
        if bg_id:
            if bg_id not in all_ids:
                raise ValueError(f"Scene '{scene_id}' references missing background '{bg_id}'")
            graph[bg_id].add(scene_id)
            in_degree[scene_id] += 1
        graph.setdefault(scene_id, set())


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
        raise ValueError("Cycle detected in dependency graph. Please check for circular references.")
    return sorted_order


def get_dependency_graph(plan):
    """
    Constructs a dependency graph for all images, scenes, voiceovers, and videos in the plan.
    Handles nested dependencies and returns topologically sorted component IDs.
    """
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    all_ids = collect_all_asset_ids(plan)

    add_image_dependencies_to_graph(plan, graph, in_degree, all_ids)
    add_voiceover_dependencies_to_graph(plan, graph, in_degree, all_ids)
    add_scene_dependencies_to_graph(plan, graph, in_degree, all_ids)
    add_video_dependencies_to_graph(plan, graph, in_degree, all_ids)

    return perform_topological_sort(graph, in_degree, all_ids)
