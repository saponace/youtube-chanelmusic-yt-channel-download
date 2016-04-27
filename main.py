#! /usr/bin/env python

import youtube_dl
from youtube_dl.utils import (DateRange)
import json

date_from = '20160422'


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
    # 'quiet': True,
    # Download videos since
    'daterange': DateRange(date_from, '99991231'),
    # Do not extract videos from playlists
    # 'extractflat': True
    'simulate': True
    }

ydl = youtube_dl.YoutubeDL(ydl_opts)
result = ydl.extract_info('https://www.youtube.com/channel/UCohPRL-xLiPQqPt-hYNU44Q')


# Can be a playlist or a list of videos
if 'entries' in result:
    print("Mock: create a playlist")

# Just a video
else:
    json_result = json.loads(json.dumps(result))
    print("Title: " + json_result['title'])
