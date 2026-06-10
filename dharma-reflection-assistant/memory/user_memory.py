import json
from pathlib import Path

MEMORY_FILE = "memory.json"

DEFAULT_PROFILE = {
    "anger": 0,
    "conflict": 0,
    "dishonesty": 0,
    "leadership": 0,
    "compassion": 0,
    "self_control": 0,
    "dharma": 0
}


def load_memory():
    if not Path(MEMORY_FILE).exists():
        return DEFAULT_PROFILE.copy()

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(profile):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)


def update_profile(profile, scores):

    profile["dharma"] += scores.get(
        "dharma",
        0
    )

    if scores.get("ego", 0) > 7:
        profile["conflict"] += 1

    if scores.get("self_control", 0) < 4:
        profile["anger"] += 1

    if scores.get("satya", 0) < 4:
        profile["dishonesty"] += 1

    if scores.get("karuna", 0) > 7:
        profile["compassion"] += 1

    if scores.get("responsibility", 0) > 7:
        profile["leadership"] += 1

    return profile


def dominant_pattern(profile):

    filtered = {
        k: v
        for k, v in profile.items()
        if isinstance(v, int)
    }

    return max(
        filtered,
        key=filtered.get
    )