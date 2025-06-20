from typing import Optional, List, Set
from data_models.Asset import Asset
import logging
import os

class Video(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy or {}
        self.sequence = self.creation_strategy.get("sequence", [])
        self.title = self.creation_strategy.get("title")
        self.style = self.creation_strategy.get("style")

    def get_dependencies(self) -> List[str]:
        return self.sequence or []

    def validate(self, all_ids: Set[str]):
        logging.info(f"Validating Video: {self.id}")
        if not self.uri and not self.creation_strategy:
            raise ValueError(f"Video '{self.id}' must have either a uri or a creation_strategy.")

        sequence = self.creation_strategy.get("sequence")
        if not sequence or not isinstance(sequence, list):
            raise ValueError(f"Video '{self.id}' must include a valid 'sequence' list in creation_strategy.")
        logging.info(f"Video '{self.id}' sequence OK: {sequence}")

        for scene_id in sequence:
            if scene_id not in all_ids:
                raise ValueError(f"Video '{self.id}' references missing scene '{scene_id}'")
            logging.info(f"Video '{self.id}' dependency OK: {scene_id}")

    def get_config(self) -> dict:
        # return super().get_config()
        return {"tool": "video_editor"}

    def set_context(self, requirements, config):
        # return super().set_context(requirements, config)
        self.requirements = requirements
        self.config = config

    def generate(self):
        try:
            # Try base class logic first (file system retrieval etc.)
            return super().generate()
        except (FileNotFoundError, NotImplementedError):
            # If base class cannot generate, do Video-specific generation
            sequence = ", ".join(self.sequence) if self.sequence else "No scenes provided"
            return f"Generated video by combining scenes: {sequence}"

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
