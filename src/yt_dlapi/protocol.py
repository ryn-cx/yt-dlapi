from typing import Any, Protocol

from pydantic import BaseModel


class YTDLAPIProtocol(Protocol):
    def yt_dlp_request(
        self,
        url: str,
        *,
        process: bool = True,
    ) -> dict[str, Any]: ...

    def parse_response[T: BaseModel](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T: ...
