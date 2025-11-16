import logging
from logging import Logger
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError
from yt_dlp import YoutubeDL
from gapi import GapiCustomizations
from .channel import ChannelMixin
from .channel.models import Channel
from .channel_playlists import ChannelPlaylistsMixin
from .channel_playlists.models import ChannelPlaylists
from .playlist import PlaylistMixin
from .playlist.models import Playlist
from .playlist_videos import PlaylistVideosMixin
from .playlist_videos.models import PlaylistVideos
from .update_files import save_file, update_model
from .video import VideoMixin
from .video.models import Video

RESPONSE_MODELS = Channel | Playlist | PlaylistVideos | Video | ChannelPlaylists
default_logger = logging.getLogger(__name__)


class YTDLAPI(
    ChannelMixin,
    PlaylistMixin,
    VideoMixin,
    ChannelPlaylistsMixin,
    PlaylistVideosMixin,
):
    def __init__(
        self,
        cookie_file: Path | None = None,
        *,
        logger: Logger = default_logger,
        verbose: bool = False,
    ) -> None:
        self.cookie_file = cookie_file
        self.verbose = verbose
        self.logger = logger

    def _yt_dlp_request(
        self,
        url: str,
        *,
        process: bool = True,
        extract_flat: bool = True,
    ) -> dict[str, Any]:
        self.logger.info("Downloading %s", url)

        opts: dict[str, Any] = {}

        # extract_flat determines how deep information should be downloaded. If True
        # when downloading something like a playlist only basic information about the
        # episodes will be downloaded, when False full information about each episode
        # will be downloaded.
        if extract_flat:
            opts["extract_flat"] = extract_flat

        if self.verbose:
            opts["verbose"] = True

        opts["logger"] = self.logger

        # Try downloading the information without cookies.
        try:
            with YoutubeDL(opts) as ytdl:
                # Process determines whether or not child information is a generator
                # object or the actual information.
                raw_json = ytdl.extract_info(url, download=False, process=process)
                return ytdl.sanitize_info(raw_json)

        # If it looks like adding cookies will help try downloading the information
        # again with cookies.
        except Exception as e:
            if self.cookie_file and "Sign in to confirm your age" in str(e):
                opts["cookiefile"] = str(self.cookie_file)
                with YoutubeDL(opts) as ytdl:
                    raw_json = ytdl.extract_info(url, download=False, process=process)
                    return ytdl.sanitize_info(raw_json)

            raise

    def _parse_response[T: RESPONSE_MODELS](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
        customizations: GapiCustomizations | None = None,
    ) -> T:
        try:
            parsed = response_model.model_validate(data)
        except ValidationError as e:
            save_file(name, data)
            update_model(name, customizations)
            msg = "Parsing error, model updated, try again."
            raise ValueError(msg) from e

        if self.dump_response(parsed) != data:
            msg = "Parsed response does not match original response."
            raise ValueError(msg)

        return parsed

    def dump_response(self, data: RESPONSE_MODELS) -> dict[str, Any]:
        """Dump an API response to a JSON serializable object."""
        return data.model_dump(mode="json", by_alias=True, exclude_unset=True)
