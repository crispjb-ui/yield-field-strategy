from __future__ import annotations
import os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = ROOT / "config" / "settings.yaml"
SETTINGS_EXAMPLE = ROOT / "config" / "settings.example.yaml"
MECHANICS = ROOT / "config" / "mechanics.yaml"


def load_settings(path: Path | None = None) -> dict:
    p = Path(path) if path else (SETTINGS if SETTINGS.exists() else SETTINGS_EXAMPLE)
    with open(p) as f:
        cfg = yaml.safe_load(f) or {}
    key = os.environ.get("OPENSEA_API_KEY")
    if key:
        cfg.setdefault("opensea", {})["api_key"] = key
    return cfg


def load_mechanics(path: Path | None = None) -> dict:
    with open(Path(path) if path else MECHANICS) as f:
        return yaml.safe_load(f) or {}
