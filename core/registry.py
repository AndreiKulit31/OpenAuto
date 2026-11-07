import json
from pathlib import Path

from functions.folders import (
    create_folder,
    del_folder,
    ren_folder,
    move,
    copy,
    list_contents,
)

from functions.control import (
    see,
    move_mouse,
    click,
    keyboard_type,
)

from functions.web_search import (
    search_web,
    search_videos,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = PROJECT_DIR / "registry.json"

TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}

FUNCTION_MAP = {
    "create_folder": create_folder,
    "del_folder": del_folder,
    "ren_folder": ren_folder,
    "move": move,
    "copy": copy,
    "search_web": search_web,
    "search_videos": search_videos,
    "list_contents": list_contents,
    "see": see,
    "move_mouse": move_mouse,
    "click": click,
    "keyboard_type": keyboard_type,
}

def load_registry():
    with REGISTRY_FILE.open("r", encoding="utf-8") as file:
        metadata = json.load(file)

    registry = {}

    for name, details in metadata.items():
        if name not in FUNCTION_MAP:
            raise ValueError(f"Unknown registered function: {name}")

        parameters = {}

        for parameter, info in details["parameters"].items():
            type_name = info["type"]

            if type_name not in TYPE_MAP:
                raise ValueError(
                    f"Unknown parameter type: {type_name}"
                )

            parameters[parameter] = {
                **info,
                "type": TYPE_MAP[type_name],
            }

        registry[name] = {
            **details,
            "function": FUNCTION_MAP[name],
            "parameters": parameters,
        }

    return registry


FUNCTION_REGISTRY = load_registry()