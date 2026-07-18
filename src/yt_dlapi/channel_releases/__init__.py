# TODO: Validate
"""Contains the ChannelReleases class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel_releases.models import ChannelReleasesModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class ChannelReleases(BaseEndpoint[ChannelReleasesModel]):
    """Manage the channel releases file."""

    _response_model = ChannelReleasesModel

    @staticmethod
    def has_content(response: dict[str, Any]) -> bool:
        """Return whether the releases tab lists at least one release."""
        return bool(response.get("entries"))

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
        """Downloads channel releases data for a given channel name.

        Args:
            channel_name: The name of the channel to download releases for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/{channel_name}/releases"
        return self._client.download(
            url,
            log_id=self.get_log_id(channel_name=channel_name),
            process=True,
            extract_flat=True,
        )

    def download_by_id(self, channel_id: str) -> dict[str, Any]:
        """Downloads channel releases data for a given channel ID.

        Args:
            channel_id: The ID of the channel to download releases for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/channel/{channel_id}/releases"
        return self._client.download(
            url,
            log_id=self.get_log_id(channel_id=channel_id),
            process=True,
            extract_flat=True,
        )

    def download_and_parse_by_name(self, channel_name: str) -> ChannelReleasesModel:
        """Downloads and parses channel releases data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get releases for.

        Returns:
            A ChannelReleases model containing the parsed data.

        Raises:
            NoContentError: If the releases tab lists nothing. The raw response
                is available on the exception's ``response`` attribute.
        """
        return self._parse_or_raise(
            self.download_by_name(channel_name),
            self.get_log_id(channel_name=channel_name),
        )

    def download_and_parse_by_id(self, channel_id: str) -> ChannelReleasesModel:
        """Downloads and parses channel releases data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get releases for.

        Returns:
            A ChannelReleases model containing the parsed data.

        Raises:
            NoContentError: If the releases tab lists nothing. The raw response
                is available on the exception's ``response`` attribute.
        """
        return self._parse_or_raise(
            self.download_by_id(channel_id),
            self.get_log_id(channel_id=channel_id),
        )
