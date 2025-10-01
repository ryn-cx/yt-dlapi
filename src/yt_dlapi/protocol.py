from typing import Any, Protocol

from pydantic import BaseModel


class YTDLAPIProtocol(Protocol):
    def _yt_dlp_request(
        self,
        url: str,
        *,
        process: bool = False,
        extract_flat: bool = True,
    ) -> dict[str, Any]: ...

    def _parse_response[T: BaseModel](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
    ) -> T: ...
