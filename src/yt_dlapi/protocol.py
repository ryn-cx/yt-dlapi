from typing import TYPE_CHECKING, Any, Protocol

from gapi import GapiCustomizations

if TYPE_CHECKING:
    from yt_dlapi.__init__ import RESPONSE_MODELS


class YTDLAPIProtocol(Protocol):
    def _yt_dlp_request(
        self,
        url: str,
        *,
        process: bool = False,
        extract_flat: bool = True,
    ) -> dict[str, Any]: ...

    def parse_response[T: RESPONSE_MODELS](
        self,
        response_model: type[T],
        data: dict[str, Any],
        name: str,
        customizations: GapiCustomizations | None = None,
    ) -> T: ...
