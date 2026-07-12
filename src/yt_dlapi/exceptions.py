# TODO: Validate
"""Exceptions for the yt-dlapi library."""

from __future__ import annotations

from typing import Any


class YTDLAPIError(Exception):
    """Base exception for the yt-dlapi library."""


class NoContentError(YTDLAPIError):
    """Raised when a download succeeds but has no meaningful content."""

    def __init__(
        self,
        response: dict[str, Any],
        log_id: str,
    ) -> None:
        """Store the downloaded response so it can be recovered by the caller."""
        self.response = response
        super().__init__(f"Response has no content for {log_id}.")
