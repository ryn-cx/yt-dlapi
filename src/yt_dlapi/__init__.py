# TODO: Validate
"""Contains the YTDLAPI class."""

import json
import time
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
    """YouTube API wrapper."""

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
        log_id: str,
        process: bool = False,
        extract_flat: bool = False,
    ) -> dict[str, Any]:
        """Make a request to yt-dlp with the given URL and options."""
        operation = f"{url} ({log_id}, extract_flat={extract_flat}, process={process})"
        logger.debug("Downloading: %s", operation)
        start = time.monotonic()

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

            logger.debug("Downloaded %s (%.4f s)", operation, time.monotonic() - start)
            return output

    def download_html(self, url: str) -> str:
        """Download the raw HTML of a URL using yt-dlp's HTTP layer."""
        operation = f"HTML {url}"
        logger.debug("Downloading: %s", operation)
        start = time.monotonic()

        with YoutubeDL({"quiet": True}) as ytdl:
            response = ytdl.urlopen(url)
            html = response.read().decode("utf-8", "replace")
            logger.debug("Downloaded %s (%.4f s)", operation, time.monotonic() - start)
            return html

    def download_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POSTs a JSON payload to a URL and returns the decoded JSON response."""
        operation = f"JSON {url}"
        logger.debug("Downloading: %s", operation)
        start = time.monotonic()

        with YoutubeDL({"quiet": True}) as ytdl:
            request = Request(
                url,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
            )
            response = ytdl.urlopen(request)
            result = json.loads(response.read().decode("utf-8", "replace"))
            logger.debug("Downloaded %s (%.4f s)", operation, time.monotonic() - start)
            return result
