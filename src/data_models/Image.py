from data_models.Asset import Asset
from typing import List, Set, Optional
import logging
import os

class Image(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy

    def get_dependencies(self) -> List[str]:
        # Return an empty list unconditionally to avoid accidental dependency IDs from YAML values.
        return []

    def validate(self, all_ids: Set[str]):
        logging.info(f"Validating Image: {self.id}")
        if not self.uri and not self.creation_strategy:
            raise ValueError(f"Image '{self.id}' must have either a uri or a creation_strategy.")

        if self.creation_strategy:
            if "prompt" not in self.creation_strategy or not isinstance(self.creation_strategy["prompt"], str):
                raise ValueError(f"Image '{self.id}' creation_strategy must include a non-empty 'prompt' string.")
            logging.info(f"Image '{self.id}' prompt OK")

    def get_config(self) -> dict:
        # return super().get_config()
        # If you want to delegate to the base Asset class, use: super().get_config()
        return {"tool": "dalle"}


    def generate(self):
        try:
            # Try base class logic first (file system retrieval etc.)
            return super().generate()
        except (FileNotFoundError, NotImplementedError):
            # If base class cannot generate, do Image-specific generation
            prompt = self.creation_strategy.get("prompt") if self.creation_strategy else "No prompt"
            return f"Generated image based on prompt: {prompt}"

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Image"]:
        images = []
        for image in plan.get("images", []):
            top_level = {
                "id": image["id"],
                "description": image["description"],
                "uri": image.get("uri")
            }
            creation_strategy = image.get("creation_strategy", {})
            images.append(cls(**top_level, creation_strategy=creation_strategy))
        return images