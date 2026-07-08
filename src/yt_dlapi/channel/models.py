# ruff: noqa: D100, D101, D102, TC001, TC002, TC003
from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict, Field


class Thumbnail(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    height: int | None = None
    width: int | None = None
    id: str | None = None
    preference: int | None = None


class FieldVersion(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    current_git_head: None
    release_git_head: str
    repository: str


class Params(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    extract_flat: bool
    process: bool


class YtDlapi(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    timestamp: AwareDatetime
    url: str
    params: Params


class ChannelModel(GAPIBaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    channel: str
    channel_id: str
    title: str
    availability: None
    channel_follower_count: int
    description: str
    tags: list[str]
    thumbnails: list[Thumbnail]
    uploader_id: str
    uploader_url: str
    modified_date: None
    view_count: None
    playlist_count: None
    uploader: str
    channel_url: str
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
