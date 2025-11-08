import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError
from yt_dlp import YoutubeDL

from .channel import ChannelMixin
from .channel.models import Channel
from .channel_playlists import ChannelPlaylistsMixin
from .channel_playlists.models import ChannelPlaylists
from .playlist import PlaylistMixin
from .playlist.models import Playlist
from .playlist_videos import PlaylistVideosMixin
from .playlist_videos.models import PlaylistVideos
from .update_files import add_test_file, update_model
from .video import VideoMixin
from .video.models import Video

RESPONSE_MODELS = Channel | Playlist | PlaylistVideos | Video | ChannelPlaylists
logger = logging.getLogger(__name__)


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
        extractor_args: dict[str, dict[str, Any]] | None = None,
        *,
        yt_dlp_logger: Any = None,
        verbose: bool = False,
    ) -> None:
        self.cookie_file = cookie_file
        self.extractor_args = extractor_args
        self.verbose = verbose
        self.yt_dlp_logger = yt_dlp_logger

    def _yt_dlp_request(
        self,
        url: str,
        *,
        process: bool = False,
        extract_flat: bool = True,
    ) -> dict[str, Any]:
        logger.info("Downloading %s", url)

        # This will minimize downloading information at depth. So if a playlist is being
        # downloaded the in depth video information is skipped.
        opts: dict[str, Any] = {"extract_flat": extract_flat}

        if self.verbose:
            opts["verbose"] = True

        if self.yt_dlp_logger is not None:
            opts["logger"] = self.yt_dlp_logger

        if self.extractor_args:
            opts["extractor_args"] = self.extractor_args

        # Try downloading the information without cookies.
        try:
            with YoutubeDL(opts) as ytdl:
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

    def _parse_response[T: BaseModel](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T:
        try:
            return response_model.model_validate(data)
        except ValidationError as e:
            add_test_file(name, data)
            update_model(name)
            msg = "Parsing error, models updated, try again."
            raise ValueError(msg) from e

    def dump_response(self, data: RESPONSE_MODELS) -> dict[str, Any]:
        """Dump an API response to a JSON serializable object."""
        return data.model_dump(mode="json", by_alias=True, exclude_unset=True)
