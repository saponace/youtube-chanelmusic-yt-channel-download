#! /usr/bin/env python

import youtube_dl
import json

date_from = '2015042'
# channel_url = 'https://www.youtube.com/channel/UCohPRL-xLiPQqPt-hYNU44Q'
channel_url = 'https://www.youtube.com/channel/UCJRljQ8OcyfzHBYpS_bDbow'


ydl_opts = {
    'format': 'bestaudio/best', # Best audio format
    'postprocessors': [{  # Post processor
        'key': 'FFmpegExtractAudio',  # Converter executable name
        'preferredcodec': 'mp3',  # Prefered codec, if available
        'preferredquality': '256',  # Prefered quality, if available
    }],
    # 'quiet': True,  # Do not print useless output
    # 'verbose': True,  # Verbose
    # 'simulate': True,  # Do not download the videos, but act as if
    'download_archive': "download-archive.txt" # Maintain a archive file of all the
                                                # already downloaded videos to avoid
                                                # downloading them several times
    }

ydl = youtube_dl.YoutubeDL(ydl_opts)

dict_result = ydl.extract_info(channel_url,
                               download=False
                              )
channel_content_dict = json.loads(json.dumps(dict_result))
for item in channel_content_dict['entries']:
    print("Downloaded: " + item['title'] + " uploaded at " + item['upload_date'])
