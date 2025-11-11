import json
import uuid
from typing import Any

from gapi import INPUT_TYPE, update_json_schema_and_pydantic_model

from yt_dlapi.constants import FILES_PATH, YT_DLAPI_PATH


def update_model(name: str, data: INPUT_TYPE) -> None:
    """Update a specific response model based on input data."""
    schema_path = YT_DLAPI_PATH / f"{name}/schema.json"
    model_path = YT_DLAPI_PATH / f"{name}/models.py"
    update_json_schema_and_pydantic_model(data, schema_path, model_path, name)


def save_file(name: str, data: dict[str, Any]) -> None:
    """Add a new test file for a given endpoint."""
    input_folder = FILES_PATH / name
    new_json_path = input_folder / f"{uuid.uuid4()}.json"
    new_json_path.parent.mkdir(parents=True, exist_ok=True)
    new_json_path.write_text(json.dumps(data, indent=2))
