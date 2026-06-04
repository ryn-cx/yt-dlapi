# yt-dlapi

Unofficial YouTube API built on [yt-dlp](https://github.com/yt-dlp/yt-dlp).

`yt-dlapi` wraps yt-dlp and parses its raw JSON into typed [Pydantic](https://docs.pydantic.dev/) models, giving you a small, structured API for reading data about YouTube videos, channels, and playlists.

## Installation

```bash
uv add git+https://github.com/ryn-cx/yt-dlapi
```

## Usage

Create a client, then call `get(...)` on an endpoint to download from YouTube and
get back a parsed, typed model.

```python
from yt_dlapi import YTDLAPI

client = YTDLAPI()

# A single video, by video ID.
video = client.video.get("jNQXAC9IVRw")

# A channel, by handle/name or by channel ID.
channel = client.channel.get_by_name("jawed")
channel = client.channel.get_by_id("UC4QobU6STFB0P71PMvOGN5A")

# A playlist, by playlist ID.
playlist = client.playlist.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")

# All playlists belonging to a channel, by handle/name or by channel ID.
playlists = client.channel_playlists.get_by_name("jawed")
playlists = client.channel_playlists.get_by_id("UC4QobU6STFB0P71PMvOGN5A")

# The videos in a playlist. Accepts a normal playlist ID (PL...) or a
# channel-derived uploads playlist ID (UU...).
videos = client.playlist_videos.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")
videos = client.playlist_videos.get("UU4QobU6STFB0P71PMvOGN5A")
```
