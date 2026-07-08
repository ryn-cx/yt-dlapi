# TODO: Validate
"""YTDLAPI is a client for downloading and parsing data from YouTube."""

import json
from datetime import datetime
from logging import NullHandler, getLogger
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.networking import Request

from yt_dlapi.channel import Channel
from yt_dlapi.channel_playlists import ChannelPlaylists
from yt_dlapi.channel_releases import ChannelReleases
from yt_dlapi.playlist import Playlist
from yt_dlapi.playlist_videos import PlaylistVideos
from yt_dlapi.video import Video

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class YTDLAPI:
    """Interface for downloading and parsing data from YouTube."""

    def __init__(self) -> None:
        """Initialize the YTDLAPI client."""
        self.channel = Channel(self)
        self.channel_playlists = ChannelPlaylists(self)
        self.channel_releases = ChannelReleases(self)
        self.playlist = Playlist(self)
        self.playlist_videos = PlaylistVideos(self)
        self.video = Video(self)

        super().__init__()

    def download(
        self,
        url: str,
        *,
        process: bool = False,
        extract_flat: bool = False,
    ) -> dict[str, Any]:
        """Make a request to yt-dlp with the given URL and options."""
        logger.info("Downloading %s", url)

        # extract_flat determines how deep information should be downloaded. If True
        # when downloading something like a playlist only basic information about the
        # episodes will be downloaded, when False full information about each episode
        # will be downloaded.

        # YoutubeDL will modify params, so pass a fresh dict each time.
        with YoutubeDL({"extract_flat": extract_flat}) as ytdl:
            # Process determines whether or not child information is a generator
            # object or the actual information.
            raw_json = ytdl.extract_info(url, download=False, process=process)
            sanitized = ytdl.sanitize_info(raw_json)

            if sanitized is None:
                msg = f"yt-dlp returned no data for {url}"
                raise ValueError(msg)

            timestamp = datetime.now().astimezone().isoformat().replace("+00:00", "Z")
            output: dict[str, Any] = dict(sanitized)
            output["yt_dlapi"] = {
                "timestamp": timestamp,
                "url": url,
                "params": {"extract_flat": extract_flat, "process": process},
            }

            return output

    def download_html(self, url: str) -> str:
        """Download the raw HTML of a URL using yt-dlp's HTTP layer.

        Used to scrape data that yt-dlp's extractors do not expose (for example the
        auto-generated album and single playlists on a Topic channel's home page).

        Args:
            url: The URL to fetch.

        Returns:
            The decoded HTML of the page.
        """
        logger.info("Downloading HTML %s", url)

        with YoutubeDL({"quiet": True}) as ytdl:
            response = ytdl.urlopen(url)
            return response.read().decode("utf-8", "replace")

    def download_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POSTs a JSON payload to a URL and returns the decoded JSON response.

        Used to call YouTube's internal InnerTube API (for example to page through a
        Topic channel's full list of album and single playlists).

        Args:
            url: The URL to POST to.
            payload: The JSON body to send.

        Returns:
            The decoded JSON response.
        """
        logger.info("Downloading JSON %s", url)

        with YoutubeDL({"quiet": True}) as ytdl:
            request = Request(
                url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
            )
            response = ytdl.urlopen(request)
            return json.loads(response.read().decode("utf-8", "replace"))
