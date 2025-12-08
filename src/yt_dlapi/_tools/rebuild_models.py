from yt_dlapi import YTDLAPI

if __name__ == "__main__":
    client = YTDLAPI()
    client.rebuild_models("channel")
    client.rebuild_models("channel_playlists")
    client.rebuild_models("playlist")
    client.rebuild_models("playlist_videos")
    client.rebuild_models("video")
