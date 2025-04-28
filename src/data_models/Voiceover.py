from data_models.Asset import Asset
from typing import Optional, List, Set
import logging
import os

class Voiceover(Asset):
    def __init__(self, id: str, description: str, text: str, uri: Optional[str] = None):
        super().__init__(id, description, uri)
        self.text = text

    def get_dependencies(self) -> List[str]:
        return []

    def validate(self, all_ids: Set[str]):
        logging.info(f"Validating Voiceover: {self.id}")
        if self.uri:
            if not isinstance(self.uri, str) or not self.uri.strip():
                logging.error(f"Voiceover '{self.id}' has an invalid uri.")
                raise ValueError(f"Voiceover '{self.id}' must have a valid uri if provided.")
            logging.info(f"Voiceover '{self.id}' using URI: {self.uri}")
        elif self.text:
            if not isinstance(self.text, str) or not self.text.strip():
                logging.error(f"Voiceover '{self.id}' has invalid text.")
                raise ValueError(f"Voiceover '{self.id}' must contain non-empty text if no uri is provided.")
            logging.info(f"Voiceover '{self.id}' has inline text.")
        else:
            logging.error(f"Voiceover '{self.id}' must have either a uri or text.")
            raise ValueError(f"Voiceover '{self.id}' must have either a uri or text.")

    def get_config(self) -> dict:
        # return super().get_config()
        return {"tool": "tts_engine"}

    def set_context(self, requirements, config):
        # return super().set_context(requirements, config)
        self.requirements = requirements
        self.config = config

    def generate(self):
        try:
            # Try base class logic first (file system retrieval etc.)
            return super().generate()
        except (FileNotFoundError, NotImplementedError):
            # If base class cannot generate, do Voiceover-specific generation
            return f"Generated voiceover based on text: {self.text}"

    @classmethod
    def load_from_plan(cls, plan: dict) -> List["Voiceover"]:
        voiceovers = []
        for vo in plan.get("voiceovers", []):
            voiceovers.append(cls(
                id=vo["id"],
                description=vo["description"],
                text=vo["text"],
                uri=vo.get("uri")
            ))
        return voiceovers