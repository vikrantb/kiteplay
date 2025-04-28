from typing import Optional, List, Set
from data_models.Asset import Asset
import logging
import os

class Scene(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy or {}

    def get_dependencies(self) -> List[str]:
        deps = []
        bg = self.creation_strategy.get("background")
        if bg:
            deps.append(bg)
        vo = self.creation_strategy.get("voiceover")
        if vo and isinstance(vo, str) and " " not in vo:
            deps.append(vo)
        return deps

    def validate(self, all_ids: Set[str]):
        logging.info(f"Validating Scene: {self.id}")

        if not self.uri and not self.creation_strategy:
            raise ValueError(f"Scene '{self.id}' must have either a uri or a creation_strategy.")

        bg = self.creation_strategy.get("background")
        if not bg:
            raise ValueError(f"Scene '{self.id}' is missing 'background' in creation_strategy.")
        if bg not in all_ids:
            raise ValueError(f"Scene '{self.id}' references missing background '{bg}'")
        logging.info(f"Scene '{self.id}' background OK: {bg}")

        scene_type = self.creation_strategy.get("type")
        if scene_type not in {"narration", "visual_only", "dialogue"}:
            raise ValueError(f"Scene '{self.id}' must specify a valid 'type' in creation_strategy.")
        logging.info(f"Scene '{self.id}' type OK: {scene_type}")

        if "text" not in self.creation_strategy:
            raise ValueError(f"Scene '{self.id}' must include 'text' in creation_strategy.")
        logging.info(f"Scene '{self.id}' text OK")

        vo = self.creation_strategy.get("voiceover")
        if vo and isinstance(vo, str) and " " not in vo:
            if vo not in all_ids:
                raise ValueError(f"Scene '{self.id}' references missing voiceover '{vo}'")
            logging.info(f"Scene '{self.id}' voiceover OK: {vo}")

    def get_config(self) -> dict:
        # return super().get_config()
        return {"tool": "scene_composer"}


    def generate(self):
        # return super().generate()
        if self.uri and self.uri.startswith("file://"):
            path = self.uri.replace("file://", "")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return f.read()
            else:
                raise FileNotFoundError(f"Scene file not found: {path}")
        else:
            text = self.creation_strategy.get("text", "No text provided")
            return f"Generated scene based on text: {text}"

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Scene"]:
        scenes = []
        for scene in plan.get("scenes", []):
            top_level = {
                "id": scene["id"],
                "description": scene["description"],
                "uri": scene.get("uri")
            }
            creation_strategy = scene.get("creation_strategy", {})
            scenes.append(cls(**top_level, creation_strategy=creation_strategy))
        return scenes