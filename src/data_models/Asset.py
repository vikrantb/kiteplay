from abc import ABC, abstractmethod
from typing import List, Set, Optional
import os
import logging

class Asset(ABC):
    def __init__(self, id: str, description: str, uri: Optional[str] = None):
        self.id = id
        self.description = description
        self.uri = uri

    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Return a list of asset IDs this object depends on."""
        pass

    @abstractmethod
    def validate(self, all_ids: Set[str]):
        """Validate internal references (like dependencies) exist in provided ID set."""
        pass

    def get_ordered_assets_from_plan(self):
        """Retrieve the asset content from the URI if available."""
        if not self.uri:
            return None
        if self.uri.startswith("file://"):
            path = self.uri.replace("file://", "")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return f.read()
        # Placeholder for future extensions: s3://, gs:// etc.
        raise NotImplementedError(f"URI scheme not supported or not implemented: {self.uri}")

    def get_config(self) -> dict:
        """Return system-level configuration for asset generation."""
        return {}

    def set_context(self, requirements: dict, config: dict):
        """Set up context for generation; can be overridden by subclasses."""
        self.requirements = requirements
        self.config = config

    def generate(self) -> str:
        """Default generate behavior: retrieve content from filesystem if URI is available."""
        if self.uri and self.uri.startswith("file://"):
            path = self.uri.replace("file://", "")
            if os.path.exists(path):
                with open(path, "r") as f:
                    return f.read()
            else:
                raise FileNotFoundError(f"Asset file not found: {path}")
        raise NotImplementedError(f"Generate method not implemented for asset: {self.id}")

