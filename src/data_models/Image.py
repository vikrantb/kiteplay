from data_models.Asset import Asset
from typing import List, Set, Optional

class Image(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy

    def dependencies(self) -> List[str]:
        return []

    def validate(self, all_ids: Set[str]):
        pass

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Image"]:
        images = []
        for image in plan.get("images", []):
            top_level = {
                "id": image["id"],
                "description": image["description"],
                "uri": image.get("uri")
            }
            creation_strategy = {k: v for k, v in image.items() if k not in ["id", "description", "uri"]}
            images.append(cls(**top_level, creation_strategy=creation_strategy))
        return images