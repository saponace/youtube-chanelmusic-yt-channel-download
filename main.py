#! /usr/bin/env python

import youtube_dl
import json


ydl_opts = {
    'format': 'bestaudio/best',
    # Post processor
    'postprocessors': [{
        # Converter executable name
        'key': 'FFmpegExtractAudio',
        # Prefered codec, if available
        'preferredcodec': 'mp3',
        # Prefered quality, if available
        'preferredquality': '256',
    }],
    # Do not print useless output
    'quiet': True,
    # Download videos since
    'dateafter': 'now-10days',
    # Do not extract videos from playlists
    'flatplaylist': True
    }

ydl = youtube_dl.YoutubeDL(ydl_opts)
result = ydl.extract_info(
    # 'https://www.youtube.com/watch?v=nsIaibmkAbI',
    'https://www.youtube.com/channel/UCohPRL-xLiPQqPt-hYNU44Q',
    download=False)


# Can be a playlist or a list of videos
if 'entries' in result:
    print("Mock: create a playlist")

# Just a video
else:
    json_result = json.loads(json.dumps(result))
    print("Title: " + json_result['title'])
