"""YTDLAPI is a client for downloading and parsing data from YouTube."""

import logging
from datetime import datetime
from logging import Logger
from typing import Any

from yt_dlp import YoutubeDL

from yt_dlapi.base_api_endpoint import BaseExtractor
from yt_dlapi.channel import Channel
from yt_dlapi.channel_playlists import ChannelPlaylists
from yt_dlapi.playlist import Playlist
from yt_dlapi.playlist_videos import PlaylistVideos
from yt_dlapi.video import Video

default_logger = logging.getLogger(__name__)


def response_models() -> list[BaseExtractor[Any]]:
    """Returns a list of all of the response models for YTDLAPI."""
    ytdlapi = YTDLAPI()

    return [
        ytdlapi.channel,
        ytdlapi.channel_playlists,
        ytdlapi.playlist,
        ytdlapi.playlist_videos,
        ytdlapi.video,
    ]


class YTDLAPI:
    """Interface for downloading and parsing data from YouTube."""

    def __init__(self, logger: Logger = default_logger) -> None:
        """Initialize the YTDLAPI client."""
        self.logger = logger

        self.channel = Channel(self)
        self.channel_playlists = ChannelPlaylists(self)
        self.playlist = Playlist(self)
        self.playlist_videos = PlaylistVideos(self)
        self.video = Video(self)

        super().__init__()

    def download_yt_dlp_request(
        self,
        url: str,
        *,
        process: bool = False,
        extract_flat: bool = False,
    ) -> dict[str, Any]:
        """Make a request to yt-dlp with the given URL and options."""
        self.logger.info("Downloading %s", url)

        # extract_flat determines how deep information should be downloaded. If True
        # when downloading something like a playlist only basic information about the
        # episodes will be downloaded, when False full information about each episode
        # will be downloaded.
        params = {"extract_flat": extract_flat}

        # params.copy() is required because YoutubeDL will modify params
        with YoutubeDL(params.copy()) as ytdl:
            # Process determines whether or not child information is a generator
            # object or the actual information.
            raw_json = ytdl.extract_info(url, download=False, process=process)
            output = ytdl.sanitize_info(raw_json)
            output["yt_dlapi"] = {}
            output["yt_dlapi"]["date"] = datetime.now().astimezone().isoformat()
            output["yt_dlapi"]["url"] = url
            params["process"] = process
            output["yt_dlapi"]["params"] = params

            return output
