from typing import Optional, List, Set
from data_models.Asset import Asset

class Scene(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy or {}

    def dependencies(self) -> List[str]:
        deps = []
        bg = self.creation_strategy.get("background")
        if bg:
            deps.append(bg)
        vo = self.creation_strategy.get("voiceover")
        if vo:
            deps.append(vo)
        return deps

    def validate(self, all_ids: Set[str]):
        if not self.uri and not self.creation_strategy:
            raise ValueError(f"Scene '{self.id}' must have either a uri or a creation_strategy.")

        bg = self.creation_strategy.get("background")
        if not bg:
            raise ValueError(f"Scene '{self.id}' is missing 'background' in creation_strategy.")
        if bg not in all_ids:
            raise ValueError(f"Scene '{self.id}' references missing background '{bg}'")

        if self.creation_strategy.get("type") not in {"narration", "visual_only", "dialogue"}:
            raise ValueError(f"Scene '{self.id}' must specify a valid 'type' in creation_strategy.")

        if "text" not in self.creation_strategy:
            raise ValueError(f"Scene '{self.id}' must include 'text' in creation_strategy.")

        vo = self.creation_strategy.get("voiceover")
        if vo and vo not in all_ids:
            raise ValueError(f"Scene '{self.id}' references missing voiceover '{vo}'")

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