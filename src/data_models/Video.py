from typing import Optional, List, Set
from data_models.Asset import Asset

class Video(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy or {}
        self.sequence = self.creation_strategy.get("sequence", [])
        self.title = self.creation_strategy.get("title")
        self.style = self.creation_strategy.get("style")

    def dependencies(self) -> List[str]:
        return self.sequence or []

    def validate(self, all_ids: Set[str]):
        if not self.uri and not self.creation_strategy:
            raise ValueError(f"Video '{self.id}' must have either a uri or a creation_strategy.")

        sequence = self.creation_strategy.get("sequence")
        if not sequence or not isinstance(sequence, list):
            raise ValueError(f"Video '{self.id}' must include a valid 'sequence' list in creation_strategy.")

        for scene_id in sequence:
            if scene_id not in all_ids:
                raise ValueError(f"Video '{self.id}' references missing scene '{scene_id}'")

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Video"]:
        videos = []
        for video in plan.get("videos", []):
            top_level = {
                "id": video["id"],
                "description": video["description"],
                "uri": video.get("uri")
            }
            creation_strategy = video.get("creation_strategy", {})
            videos.append(cls(**top_level, creation_strategy=creation_strategy))
        return videos