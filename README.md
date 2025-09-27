<div align="center">

# 📺 YT-DLAPI

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/ryn-cx/yt-dlapi/refs/heads/master/pyproject.toml)
![GitHub License](https://img.shields.io/github/license/ryn-cx/yt-dlapi)
![GitHub Issues](https://img.shields.io/github/issues/ryn-cx/yt-dlapi)

**An unofficial YouTube API based on yt-dlp**

</div>

## ✨ Features

- 🎥 **Video, Channel & Playlist Support**: Extract detailed metadata and information from videos, channels, and playlists
- 🔄 **Dynamic Models**: Automatically updating Pydantic models based on API responses
- 🍪 **Cookie Support**: Optional cookie file support for age-restricted content
- 🛡️ **Type Safety**: Full Pydantic models for robust data validation

## 📦 Installation

### Requirements

- 🐍 Python 3.13 or higher

### Install from source

```bash
uv add git+https://github.com/ryn-cx/yt-dlapi
```

## 🚀 Quick Start

### Create Client

```python
from yt_dlapi import YTDLAPI
from pathlib import Path

# 🌐 Create client without cookies
client = YTDLAPI()

# 🍪 Create client with cookie file for age-restricted content
client = YTDLAPI(cookie_file=Path("cookies.txt"))
```

### Access API

```python
# 🎬 Get video information
video_info = client.get_video("VIDEO_ID")

# 📺 Get channel information
channel_info = client.get_channel("CHANNEL_ID")

# 📋 Get playlist information
playlist_info = client.get_playlist("PLAYLIST_ID")
```
