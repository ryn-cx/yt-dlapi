# TODO: Validate
"""Exceptions for the yt-dlapi library."""

from __future__ import annotations

from typing import Any


class YTDLAPIError(Exception):
    """Base exception for the yt-dlapi library."""


class NoContentError(YTDLAPIError):
    """Raised when a download succeeds but has no meaningful content.

    Unlike an invalid URL (which yt-dlp surfaces as a ``DownloadError``), an
    empty-but-valid response - for example a real channel whose "Releases" tab
    lists nothing - is returned by yt-dlp as ``entries: []`` without raising.
    This exception makes that "nothing here" case explicit while still keeping
    the downloaded payload recoverable.
    """

    def __init__(
        self,
        response: dict[str, Any],
        *,
        endpoint: str | None = None,
    ) -> None:
        """Store the downloaded response so it can be recovered by the caller.

        Args:
            response: The raw yt-dlp response that was found to be empty.
            endpoint: The endpoint name, included in the error message.
        """
        self.response = response
        location = f" for {endpoint}" if endpoint else ""
        super().__init__(f"Response has no content{location}.")
