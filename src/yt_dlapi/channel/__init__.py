# TODO: Validate
"""Contains the Channel class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel.models import ChannelModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Channel(BaseEndpoint[ChannelModel]):
    """Manage the channel file."""

    _response_model = ChannelModel

    def get_log_id(
        self,
        *,
        channel_name: str | None = None,
        channel_id: str | None = None,
    ) -> str:
        """Build the log id for a download."""
        return self.append_non_default_args(
            f"{self.__class__.__name__}",
            channel_name=(channel_name, None),
            channel_id=(channel_id, None),
        )

    def download_by_name(self, channel_name: str) -> dict[str, Any]:
        """Downloads channel data for a given channel name.

        Args:
            channel_name: The name of the channel to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/@{channel_name}"
        return self._client.download(
            url,
            log_id=self.get_log_id(channel_name=channel_name),
        )

    def download_by_id(self, channel_id: str) -> dict[str, Any]:
        """Downloads channel data for a given channel ID.

        Args:
            channel_id: The ID of the channel to download.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/channel/{channel_id}"
        return self._client.download(
            url,
            log_id=self.get_log_id(channel_id=channel_id),
        )

    def download_and_parse_by_name(self, channel_name: str) -> ChannelModel:
        """Downloads and parses channel data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get.

        Returns:
            A Channel model containing the parsed data.
        """
        return self.parse(self.download_by_name(channel_name))

    def download_and_parse_by_id(self, channel_id: str) -> ChannelModel:
        """Downloads and parses channel data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get.

        Returns:
            A Channel model containing the parsed data.
        """
        return self.parse(self.download_by_id(channel_id))
