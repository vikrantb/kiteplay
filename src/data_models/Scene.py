from typing import Optional, List, Set
from data_models.Asset import Asset

class Scene(Asset):
    def __init__(self, id: str, background: str, background_type: str, type: str,
                 text: str, voiceover: Optional[str] = None, duration: Optional[int] = 5):
        super().__init__(id)
        self.background = background
        self.background_type = background_type
        self.scene_type = type
        self.text = text
        self.voiceover = voiceover
        self.duration = duration

    def dependencies(self) -> List[str]:
        deps = [self.background]
        if self.voiceover:
            deps.append(self.voiceover)
        return deps

    def validate(self, all_ids: Set[str]):
        if self.background not in all_ids:
            raise ValueError(f"Scene '{self.id}' references missing background '{self.background}'")
        if self.voiceover and self.voiceover not in all_ids:
            raise ValueError(f"Scene '{self.id}' references missing voiceover '{self.voiceover}'")

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Scene"]:
        return [cls(**scene_data) for scene_data in plan.get("scenes", [])]