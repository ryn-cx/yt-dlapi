# TODO: Validate
"""Channel Playlists API endpoint."""

from __future__ import annotations

from typing import Any

from yt_dlapi.base_api_endpoint import BaseEndpoint
from yt_dlapi.channel_playlists.zzz_album_scraper import (
    browse_url,
    continuation_payload,
    extract_albums,
    extract_api_key,
    extract_client_version,
    extract_yt_initial_data,
    find_album_continuation_token,
    find_continuation_token,
)
from yt_dlapi.channel_playlists.albums import Album, ChannelAlbums
from yt_dlapi.channel_playlists.models import ChannelPlaylistsModel

# Safety cap on continuation pages, to avoid looping forever on a malformed token.
_MAX_CONTINUATION_PAGES = 50


class ChannelPlaylists(BaseEndpoint[ChannelPlaylistsModel]):
    """Provides methods to download, parse, and retrieve channel playlists data."""

    _response_model = ChannelPlaylistsModel

    def download_by_name(self, channel_name: str) -> dict[str, Any]:
        """Downloads channel playlists data for a given channel name.

        Args:
            channel_name: The name of the channel to download playlists for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/{channel_name}/playlists"
        return self._client.download(
            url,
            process=True,
            extract_flat=True,
        )

    def download_by_id(self, channel_id: str) -> dict[str, Any]:
        """Downloads channel playlists data for a given channel ID.

        Args:
            channel_id: The ID of the channel to download playlists for.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        url = f"https://www.youtube.com/channel/{channel_id}/playlists"
        return self._client.download(
            url,
            process=True,
            extract_flat=True,
        )

    def get_by_name(self, channel_name: str) -> ChannelPlaylistsModel:
        """Downloads and parses channel playlists data for a given channel name.

        Convenience method that calls ``download_by_name()`` then ``parse()``.

        Args:
            channel_name: The name of the channel to get playlists for.

        Returns:
            A ChannelPlaylists model containing the parsed data.
        """
        return self.parse(self.download_by_name(channel_name))

    def get_by_id(self, channel_id: str) -> ChannelPlaylistsModel:
        """Downloads and parses channel playlists data for a given channel ID.

        Convenience method that calls ``download_by_id()`` then ``parse()``.

        Args:
            channel_id: The ID of the channel to get playlists for.

        Returns:
            A ChannelPlaylists model containing the parsed data.
        """
        return self.parse(self.download_by_id(channel_id))

    def download_albums_by_id(self, channel_id: str) -> str:
        """Downloads the home page HTML for a channel by ID.

        Used to scrape the auto-generated album and single playlists on Topic
        channels, which yt-dlp's ``/playlists`` tab does not expose.

        Args:
            channel_id: The ID of the channel to download the home page for.

        Returns:
            The raw HTML of the channel's home page, suitable for ``parse_albums()``.
        """
        url = f"https://www.youtube.com/channel/{channel_id}"
        return self._client.download_html(url)

    def download_albums_by_name(self, channel_name: str) -> str:
        """Downloads the home page HTML for a channel by name.

        Used to scrape the auto-generated album and single playlists on Topic
        channels, which yt-dlp's ``/playlists`` tab does not expose.

        Args:
            channel_name: The name of the channel to download the home page for.

        Returns:
            The raw HTML of the channel's home page, suitable for ``parse_albums()``.
        """
        url = f"https://www.youtube.com/{channel_name}"
        return self._client.download_html(url)

    def parse_albums(self, html: str, channel_url: str) -> ChannelAlbums:
        """Parses album and single playlists out of channel home page HTML.

        The home page only renders the first batch of albums; the rest are fetched by
        paging through YouTube's InnerTube ``browse`` API using the continuation token
        embedded in the "Albums & Singles" shelf.

        Args:
            html: The raw HTML of a Topic channel's home page.
            channel_url: The URL the HTML was downloaded from.

        Returns:
            A ChannelAlbums model containing the scraped album playlists.
        """
        data = extract_yt_initial_data(html)

        albums = extract_albums(data)
        seen = {album.id for album in albums}

        albums.extend(self._follow_album_continuations(html, data, seen))

        return ChannelAlbums(channel_url=channel_url, albums=albums)

    def _follow_album_continuations(
        self,
        html: str,
        data: dict[str, Any],
        seen: set[str],
    ) -> list[Album]:
        """Page through the InnerTube API for albums beyond the first home page batch.

        Args:
            html: The raw home page HTML (source of the API key and client version).
            data: The decoded ``ytInitialData`` (source of the first continuation).
            seen: Playlist IDs already collected; updated in place as new ones arrive.

        Returns:
            The additional album playlists found across all continuation pages.
        """
        api_key = extract_api_key(html)
        client_version = extract_client_version(html)
        token = find_album_continuation_token(data)
        if not api_key or not client_version or not token:
            return []

        url = browse_url(api_key)
        extra: list[Album] = []
        for _ in range(_MAX_CONTINUATION_PAGES):
            response = self._client.download_json(
                url,
                continuation_payload(client_version, token),
            )

            new_albums = [a for a in extract_albums(response) if a.id not in seen]
            for album in new_albums:
                seen.add(album.id)
                extra.append(album)

            token = find_continuation_token(response)
            if not token:
                break

        return extra

    def get_albums_by_id(self, channel_id: str) -> ChannelAlbums:
        """Downloads and parses a channel's album and single playlists by ID.

        Convenience method that scrapes the auto-generated album playlists from a
        Topic channel's home page (yt-dlp's ``/playlists`` tab does not expose them).

        Args:
            channel_id: The ID of the channel to get album playlists for.

        Returns:
            A ChannelAlbums model containing the scraped album playlists.
        """
        url = f"https://www.youtube.com/channel/{channel_id}"
        return self.parse_albums(self.download_albums_by_id(channel_id), url)

    def get_albums_by_name(self, channel_name: str) -> ChannelAlbums:
        """Downloads and parses a channel's album and single playlists by name.

        Convenience method that scrapes the auto-generated album playlists from a
        Topic channel's home page (yt-dlp's ``/playlists`` tab does not expose them).

        Args:
            channel_name: The name of the channel to get album playlists for.

        Returns:
            A ChannelAlbums model containing the scraped album playlists.
        """
        url = f"https://www.youtube.com/{channel_name}"
        return self.parse_albums(self.download_albums_by_name(channel_name), url)
