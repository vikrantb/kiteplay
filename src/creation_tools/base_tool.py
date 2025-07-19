from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """
    Abstract base class for all AI creation tools (scene, video, voiceover, music, etc).
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def load_config(self):
        """
        Load and validate configuration (e.g., API keys, endpoints).
        Should populate necessary credentials internally.
        """
        pass

    @abstractmethod
    def setup(self):
        """
        Perform authentication or environment preparation if required.
        E.g., login, get access tokens, preload models.
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Perform the main action — e.g., generate an image, text, video, audio.
        Arguments depend on the specific tool.
        Should return a usable result (or a reference to output).
        """
        pass

    @abstractmethod
    def post_process(self, result: Any) -> Any:
        """
        Perform any clean-up, formatting, validation, retries, or post-processing.
        E.g., reformat response, save result to disk, handle errors gracefully.
        """
        pass

    def describe(self) -> Dict[str, Any]:
        """
        (Optional) Return a description of the tool (for UI or logs).
        """
        return {
            "tool_name": self.__class__.__name__,
            "description": "No description provided."
        }