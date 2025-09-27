import logging
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError
from yt_dlp import YoutubeDL

from yt_dlapi.channel import Channel
from yt_dlapi.playlist import Playlist
from yt_dlapi.update_files import Updater
from yt_dlapi.video import Video

logger = logging.getLogger(__name__)


class YTDLAPI(Channel, Playlist, Video):
    def __init__(self, cookie_file: Path | None = None) -> None:
        self.cookie_file = cookie_file

    def yt_dlp_request(self, url: str, *, process: bool = True) -> dict[str, Any]:
        logger.info("Downloading %s", url)

        # This makes it so all of the data downloaded is flat. So if a channel is
        # downloaded the videos on that channel will NOT be included.
        opts = {"extract_flat": "in_playlist"}

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

    def parse_response[T: BaseModel](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T:
        try:
            return response_model.model_validate(data)
        except ValidationError as e:
            updater = Updater(name)
            updater.add_test_file(data)
            updater.generate_schema()
            updater.remove_redundant_files()
            msg = "Parsing error, models updated, try again."
            raise ValueError(msg) from e
