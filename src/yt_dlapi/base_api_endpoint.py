# TODO: Validate
"""Base API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from yt_dlapi.constants import FILES_PATH
from yt_dlapi.exceptions import NoContentError

if TYPE_CHECKING:
    from pathlib import Path

    from yt_dlapi import YTDLAPI


class BaseExtractor[T: GAPIBaseModel](GAPIClient[T]):
    """Base class to extract data from API responses."""

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._folder_name(cls._model_name())
        return FILES_PATH / folder_name.replace("_model", "")


class BaseEndpoint[T: GAPIBaseModel](BaseExtractor[T]):
    """Base class for API endpoints."""

    def __init__(self, client: YTDLAPI) -> None:
        """Initialize the endpoint with the YTDLAPI client."""
        self._client = client

    @staticmethod
    def has_content(response: dict[str, Any]) -> bool:
        """Return whether a successful download has meaningful content.

        Defaults to ``True``. Endpoints with an empty-but-valid state - for
        example a real channel whose "Releases" tab lists nothing, which yt-dlp
        returns as ``entries: []`` without raising - override this so ``get``
        raises ``NoContentError`` instead of returning an empty model.

        Args:
            response: The raw yt-dlp response to inspect.

        Returns:
            ``True`` if the response has content, ``False`` otherwise.
        """
        return True

    def _parse_or_raise(self, response: dict[str, Any]) -> T:
        """Parse ``response``, or raise ``NoContentError`` when it is empty.

        This is the single place ``get`` decides "nothing here". The raised
        ``NoContentError`` carries ``response``, so callers can still recover
        the downloaded payload from the exception.

        Args:
            response: The raw yt-dlp response to parse.

        Returns:
            The parsed model.

        Raises:
            NoContentError: If ``has_content`` is false for ``response``.
        """
        if not self.has_content(response):
            raise NoContentError(response, endpoint=type(self).__name__)
        return self.parse(response)
