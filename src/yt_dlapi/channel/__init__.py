"""Channel API endpoint."""

from __future__ import annotations

from functools import cached_property
from typing import Any, overload, override

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel import models


class Channel(BaseEndpoint[models.Channel]):
    """Provides methods to download, parse, and retrieve channel data."""

    @cached_property
    @override
    def _response_model(self) -> type[models.Channel]:
        """Return the Pydantic model class for this client."""
        return models.Channel

    @overload
    def download(self, *, channel_name: str) -> dict[str, Any]: ...
    @overload
    def download(self, *, channel_id: str) -> dict[str, Any]: ...
    def download(
        self,
        *,
        channel_name: str | None = None,
        channel_id: str | None = None,
    ) -> dict[str, Any]:
        """Downloads channel data for a given channel name or ID.

        Args:
            channel_name: The name of the channel to download.
            channel_id: The ID of the channel to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            url = f"https://www.youtube.com/@{channel_name}"
            return self._client.download_yt_dlp_request(url)
        if channel_id:
            url = f"https://www.youtube.com/channel/{channel_id}"
            return self._client.download_yt_dlp_request(url)
        msg = "channel_name or channel_id must be provided."
        raise ValueError(msg)

    def parse(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
    ) -> models.Channel:
        """Parses channel data into a Channel model.

        Args:
            data: The channel data to parse.
            update: Whether to update models if parsing fails.

        Returns:
            A Channel model containing the parsed data.
        """
        if update:
            return self._parse_response(data)

        return models.Channel.model_validate(data)

    @overload
    def get(self, *, channel_name: str) -> models.Channel: ...
    @overload
    def get(self, *, channel_id: str) -> models.Channel: ...
    def get(
        self,
        *,
        channel_id: str | None = None,
        channel_name: str | None = None,
    ) -> models.Channel:
        """Downloads and parses channel data for a given channel name or ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get.
            channel_name: The name of the channel to get.

        Returns:
            A Channel model containing the parsed data.
        """
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            response = self.download(channel_name=channel_name)
        elif channel_id:
            response = self.download(channel_id=channel_id)
        else:
            msg = "channel_name or channel_id must be provided."
            raise ValueError(msg)

        return self.parse(response)
