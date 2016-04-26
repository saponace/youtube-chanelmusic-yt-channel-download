#! /usr/bin/env python

import youtube_dl
import json


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256',
    }],
    # 'quiet': True,
    # 'restrictfilenames': True,
    }

ydl = youtube_dl.YoutubeDL(ydl_opts)
result = ydl.extract_info(
    'https://www.youtube.com/watch?v=nsIaibmkAbI',
    download=False)

json_result = json.loads(json.dumps(result))

# Can be a playlist or a list of videos
if 'entries' in result:
    print("Mock: create a playlist")

# Just a video
else:
    print("Title: " + json_result['title'])
