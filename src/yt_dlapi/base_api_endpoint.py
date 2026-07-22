# TODO: Validate
"""Base API endpoints."""

from __future__ import annotations

from inspect import Parameter, signature
from typing import TYPE_CHECKING, Any

from good_ass_pydantic_integrator import GAPIBaseModel, GAPIClient

from yt_dlapi.constants import FILES_PATH
from yt_dlapi.exceptions import NoContentError

if TYPE_CHECKING:
    from collections.abc import Callable

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
    def non_default_args(
        func: Callable[..., Any],
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """Return the args that are changed from their default values."""
        return {
            name: values[name]
            for name, param in signature(func).parameters.items()
            if param.default is not Parameter.empty
            and name in values
            and values[name] != param.default
        }

    def get_log_id(self, func: Callable[..., Any], values: dict[str, Any]) -> str:
        """Gets the log id.

        Example: ClassName (arg1='value1' arg2='value2')
        """
        required = {
            name: values[name]
            for name, param in signature(func).parameters.items()
            if param.default is Parameter.empty and name in values
        }
        set_args = {**required, **self.non_default_args(func, values)}
        parts = [
            *(f"{name}={value!r}" for name, value in set_args.items()),
        ]
        name = self.__class__.__name__
        if not parts:
            return name
        return f"{name} ({' '.join(parts)})"

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
