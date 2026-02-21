# ruff: noqa: D100, D101
from __future__ import annotations

from typing import Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class DownloaderOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    http_chunk_size: int


class Format(BaseModel):
    model_config = ConfigDict(extra="forbid")
    asr: int | None
    filesize: int
    format_id: str
    format_note: str
    source_preference: int
    fps: int | None
    audio_channels: int | None
    height: int | None
    quality: float
    has_drm: bool
    tbr: float
    filesize_approx: int
    width: int | None
    language: None
    language_preference: int
    preference: None
    ext: str
    vcodec: str
    acodec: str
    dynamic_range: None
    url: str
    available_at: int
    downloader_options: DownloaderOptions
    container: str | None = None


class Thumbnail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str
    height: int | None = None
    width: int | None = None
    preference: int


class EnItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ext: str
    url: str
    name: str
    impersonate: bool
    field__yt_dlp_client: str = Field(..., alias="__yt_dlp_client")


class DeItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ext: str
    url: str
    name: str
    impersonate: bool
    field__yt_dlp_client: str = Field(..., alias="__yt_dlp_client")


class Subtitles(BaseModel):
    model_config = ConfigDict(extra="forbid")
    en: list[EnItem]
    de: list[DeItem]


class Chapter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start_time: float
    title: str


class HeatmapItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start_time: float
    end_time: float
    value: float


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
    timestamp: AwareDatetime
    url: str
    params: Params


class VideoModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    title: str
    formats: list[Format]
    thumbnails: list[Thumbnail]
    thumbnail: str
    description: str
    channel_id: str
    channel_url: str
    duration: int
    view_count: int
    average_rating: None
    age_limit: int
    webpage_url: str
    categories: list[str]
    tags: list[str]
    playable_in_embed: bool
    live_status: str
    media_type: str
    release_timestamp: None
    field_format_sort_fields: list[str] = Field(..., alias="_format_sort_fields")
    automatic_captions: dict[str, Any]
    subtitles: Subtitles
    comment_count: int
    chapters: list[Chapter]
    heatmap: list[HeatmapItem]
    location: str
    like_count: int
    channel: str
    channel_follower_count: int
    creators: None
    channel_is_verified: bool
    uploader: str
    uploader_id: str
    uploader_url: str
    upload_date: str
    timestamp: int
    availability: str
    field__post_extractor: None = Field(..., alias="__post_extractor")
    original_url: str
    webpage_url_basename: str
    webpage_url_domain: str
    extractor: str
    extractor_key: str
    epoch: int
    field_type: str = Field(..., alias="_type")
    field_version: FieldVersion = Field(..., alias="_version")
    yt_dlapi: YtDlapi
