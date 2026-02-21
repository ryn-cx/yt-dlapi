"""Base API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from good_ass_pydantic_integrator import GAPIClient
from pydantic import BaseModel

from yt_dlapi.constants import FILES_PATH

if TYPE_CHECKING:
    from pathlib import Path

    from yt_dlapi import YTDLAPI


class BaseExtractor[T: BaseModel](GAPIClient[T]):
    """Base class to extract data from API responses."""

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._to_folder_name(cls._get_model_name())
        return FILES_PATH / folder_name.replace("_model", "")


class BaseEndpoint[T: BaseModel](BaseExtractor[T]):
    """Base class for API endpoints."""

    def __init__(self, client: YTDLAPI) -> None:
        """Initialize the endpoint with the YTDLAPI client."""
        self._client = client
