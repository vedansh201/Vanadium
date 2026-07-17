import json
from pathlib import Path


SETTINGS_FILE = Path(__file__).parent.parent / "settings.json"


def load_settings():
    """Load settings from settings.json."""

    if not SETTINGS_FILE.exists():
        return {
            "search_engine": "bing"
        }

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)