"""Channel Releases API endpoint."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel_releases.models import ChannelReleasesModel


class ChannelReleases(BaseEndpoint[ChannelReleasesModel]):
    """Provides methods to download, parse, and retrieve channel releases data.

    A channel's "Releases" tab lists its albums and singles as playlists. Unlike the
    auto-generated "Albums & Singles" shelf on Topic channels, this tab is exposed by
    yt-dlp directly, so no HTML scraping is required.
    """

    _response_model = ChannelReleasesModel

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
            process=True,
            extract_flat=True,
        )

    def get_by_name(self, channel_name: str) -> ChannelReleasesModel:
        """Downloads and parses channel releases data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get releases for.

        Returns:
            A ChannelReleases model containing the parsed data.
        """
        return self.parse(self.download_by_name(channel_name))

    def get_by_id(self, channel_id: str) -> ChannelReleasesModel:
        """Downloads and parses channel releases data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get releases for.

        Returns:
            A ChannelReleases model containing the parsed data.
        """
        return self.parse(self.download_by_id(channel_id))
