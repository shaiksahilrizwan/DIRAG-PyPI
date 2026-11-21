import json
from pathlib import Path

try:
    from ..Exceptions.exceptions import InvalidDictKeys
except ImportError:
    from Exceptions.exceptions import InvalidDictKeys


class ConfigLoader:
    """Handle Ollama configuration stored in dirag.json."""

    def __init__(self):
        self.config = None
        config_path = Path.cwd() / "dirag.json"
        try:
            with config_path.open("r", encoding="utf-8") as fp:
                self.config = json.load(fp)
        except FileNotFoundError:
            raise
        except json.JSONDecodeError:
            self.config = None

    def get_config(self):
        """Return the configuration JSON as a dictionary."""
        try:
            if not isinstance(self.config, dict):
                raise InvalidDictKeys("Invalid configuration JSON")
            required = {"ollama_url", "model"}
            missing = required.difference(self.config)
            if missing:
                raise InvalidDictKeys(
                    "Missing configuration keys: " + ", ".join(sorted(missing))
                )
            return self.config
        except KeyError as exc:
            raise InvalidDictKeys("JSON configuration error") from exc