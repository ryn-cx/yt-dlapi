import json
import logging
import uuid
from logging import Logger
from pathlib import Path
from typing import Any, override

from gapi import (
    AbstractGapiClient,
    GapiCustomizations,
    apply_customizations,
    update_json_schema_and_pydantic_model,
)
from yt_dlp import YoutubeDL

from yt_dlapi.constants import YT_DLAPI_PATH

from .channel import ChannelMixin
from .channel.models import Channel
from .channel_playlists import ChannelPlaylistsMixin
from .channel_playlists.models import ChannelPlaylists
from .constants import FILES_PATH
from .playlist import PlaylistMixin
from .playlist.models import Playlist
from .playlist_videos import PlaylistVideosMixin
from .playlist_videos.models import PlaylistVideos
from .video import VideoMixin
from .video.models import Video

RESPONSE_MODELS = Channel | Playlist | PlaylistVideos | Video | ChannelPlaylists
default_logger = logging.getLogger(__name__)


class YTDLAPI(
    AbstractGapiClient,
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

    @override
    def save_file(self, name: str, data: dict[str, Any], model_type: str) -> None:
        """Add a new test file for a given endpoint."""
        input_folder = FILES_PATH / name
        new_json_path = input_folder / f"{uuid.uuid4()}.json"
        new_json_path.parent.mkdir(parents=True, exist_ok=True)
        new_json_path.write_text(json.dumps(data, indent=2))

    @override
    def update_model(
        self,
        name: str,
        model_type: str,
        customizations: GapiCustomizations | None = None,
    ) -> None:
        """Update a specific response model based on input data."""
        schema_path = YT_DLAPI_PATH / f"{name}/schema.json"
        model_path = YT_DLAPI_PATH / f"{name}/models.py"
        files_path = FILES_PATH / name
        update_json_schema_and_pydantic_model(files_path, schema_path, model_path, name)
        apply_customizations(model_path, customizations)
