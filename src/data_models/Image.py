from data_models.Asset import Asset
from typing import List, Set, Optional

class Image(Asset):
    def __init__(self, id: str, description: str, uri: Optional[str] = None, creation_strategy: Optional[dict] = None):
        super().__init__(id, description, uri)
        self.creation_strategy = creation_strategy

    def dependencies(self) -> List[str]:
        return []

    def validate(self, all_ids: Set[str]):
        logging.info(f"Validating Image: {self.id}")
        if not self.uri and not self.creation_strategy:
            raise ValueError(f"Image '{self.id}' must have either a uri or a creation_strategy.")

        if self.creation_strategy:
            if "prompt" not in self.creation_strategy or not isinstance(self.creation_strategy["prompt"], str):
                raise ValueError(f"Image '{self.id}' creation_strategy must include a non-empty 'prompt' string.")
            logging.info(f"Image '{self.id}' prompt OK")

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