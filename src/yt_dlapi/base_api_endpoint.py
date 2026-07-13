# TODO: Validate
"""Base API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from yt_dlapi.constants import FILES_PATH
from yt_dlapi.exceptions import NoContentError

if TYPE_CHECKING:
    from yt_dlapi import YTDLAPI


class BaseExtractor[T: GAPIBaseModel](GAPIClient[T]):
    """Base class to extract data from API responses."""

    JSON_FILES_ROOT = FILES_PATH


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

    def _parse_or_raise(self, response: dict[str, Any], log_id: str) -> T:
        """Parse `response`, or raise `NoContentError` if it is empty.

        Raises:
            NoContentError: If `has_content` is false.
        """
        if not self.has_content(response):
            raise NoContentError(response, log_id)
        return self.parse(response)
