import pytest

from yt_dlapi import YTDLAPI


@pytest.fixture(scope="session")
def client() -> YTDLAPI:
    return YTDLAPI()
