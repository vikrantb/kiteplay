from typing import Optional, List, Set
from data_models.Asset import Asset

class Video(Asset):
    def __init__(self, id: str, sequence: List[str], title: Optional[str] = None,
                 style: Optional[str] = None, description: Optional[str] = None):
        super().__init__(id)
        self.sequence = sequence
        self.title = title
        self.style = style
        self.description = description

    def dependencies(self) -> List[str]:
        return self.sequence or []

    def validate(self, all_ids: Set[str]):
        for scene_id in self.sequence:
            if scene_id not in all_ids:
                raise ValueError(f"Video '{self.id}' references missing scene '{scene_id}'")

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Video"]:
        videos = []
        for video_data in plan.get("videos", []):
            video_data.setdefault("sequence", [])
            video = cls(
                id=video_data["id"],
                sequence=video_data["sequence"],
                title=video_data.get("title"),
                style=video_data.get("style"),
                description=video_data.get("description")
            )
            videos.append(video)
        return videos