#!/usr/bin/env python3

import os
import shutil
import zipfile
import requests
import urllib.request

if os.name != 'nt':
	print("This dones't look like Windows, but what do I know.")

print("Downloading yotube-dl")
req = requests.get('https://github.com/rg3/youtube-dl/releases/latest')
version = req.url.split('/')[-1]
dl = 'https://github.com/rg3/youtube-dl/releases/download/'+version+'/youtube-dl.exe'
dest = os.path.join('yt2gif','win','youtube-dl.exe')
with urllib.request.urlopen(dl) as response, open(dest, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

print("Downloading ffmpeg")
dl = 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.0-win64-static.zip'
req = urllib.request.Request(dl, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response, open('ffmpeg.zip', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
zf = zipfile.ZipFile('ffmpeg.zip', 'r')
zf.extract('ffmpeg-4.0-win64-static/bin/ffmpeg.exe')
zf.close()
os.remove('ffmpeg.zip')
os.rename(os.path.join('ffmpeg-4.0-win64-static','bin','ffmpeg.exe'),os.path.join('yt2gif','win','ffmpeg.exe'))
shutil.rmtree('ffmpeg-4.0-win64-static')

print("Done!")
