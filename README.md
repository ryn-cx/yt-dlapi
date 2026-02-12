<div align="center">

# YT-DLAPI

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/ryn-cx/yt-dlapi/refs/heads/master/pyproject.toml)
![GitHub License](https://img.shields.io/github/license/ryn-cx/yt-dlapi)
![GitHub Issues](https://img.shields.io/github/issues/ryn-cx/yt-dlapi)

**An unofficial YouTube API based on yt-dlp**

</div>

## Features

- **Video, Channel & Playlist Support** - Extract detailed metadata from videos, channels, and playlists
- **Type Safety** - Full Pydantic models for every endpoint with robust data validation
- **Self-Updating Models** - Models are automatically updated when the API response structure changes

## Installation

Requires Python 3.13+

```bash
uv add git+https://github.com/ryn-cx/yt-dlapi
```

## Quick Start

```python
from yt_dlapi import YTDLAPI

client = YTDLAPI()
```

### Video

```python
video = client.video.get("jNQXAC9IVRw")
```

### Channel

```python
channel = client.channel.get_by_name("jawed")
channel = client.channel.get_by_id("UC4QobU6STFB0P71PMvOGN5A")
```

### Playlist

```python
playlist = client.playlist.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")
```

### Channel Playlists

```python
playlists = client.channel_playlists.get_by_name("jawed")
playlists = client.channel_playlists.get_by_id("UC4QobU6STFB0P71PMvOGN5A")
```

### Playlist Videos

```python
videos = client.playlist_videos.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")
```

## Two-Step API

Every endpoint supports a two-step `download()` / `parse()` workflow for cases where you want to inspect or cache the raw JSON before parsing:

```python
raw = client.video.download("jNQXAC9IVRw")
parsed = client.video.parse(raw)

raw = client.channel.download_by_name("jawed")
parsed = client.channel.parse(raw)
```
