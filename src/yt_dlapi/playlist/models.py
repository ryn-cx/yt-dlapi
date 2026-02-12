# ruff: noqa: D100, D101
from __future__ import annotations

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class Thumbnail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    height: int
    width: int


class FieldVersion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    current_git_head: None
    release_git_head: str
    repository: str


class Params(BaseModel):
    model_config = ConfigDict(extra="forbid")
    extract_flat: bool
    process: bool


class YtDlapi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date: AwareDatetime
    url: str
    params: Params


class Playlist(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    availability: None
    channel_follower_count: None
    description: str
    tags: list
    thumbnails: list[Thumbnail]
    modified_date: str
    view_count: int
    playlist_count: int
    channel: str
    channel_id: str
    uploader_id: str
    uploader: str
    channel_url: str
    uploader_url: str
    field_type: str = Field(..., alias="_type")
    entries: str
    extractor_key: str
    extractor: str
    webpage_url: str
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    epoch: int
    field_version: FieldVersion = Field(..., alias="_version")
    yt_dlapi: YtDlapi
