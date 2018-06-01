#!/usr/bin/env python3

import os
import shutil
import zipfile
import requests
import urllib.request

if os.name != 'nt':
	print("You don't need this, silly!")
	raise SystemExit

print("Downloading yotube-dl")
req = requests.get('https://github.com/rg3/youtube-dl/releases/latest')
version = req.url.split('/')[-1]
dl = 'https://github.com/rg3/youtube-dl/releases/download/'+version+'/youtube-dl.exe'
with urllib.request.urlopen(dl) as response, open('youtube-dl.exe', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

print("Downloading ffmpeg")
dl = 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.0-win64-static.zip'
req = urllib.request.Request(dl, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response, open('ffmpeg.zip', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
zip = zipfile.ZipFile('ffmpeg.zip', 'r')
zip.extract('ffmpeg-4.0-win64-static/bin/ffmpeg.exe')
zip.close()
os.remove('ffmpeg.zip')
os.rename('ffmpeg-4.0-win64-static\\bin\\ffmpeg.exe','ffmpeg.exe')
shutil.rmtree('ffmpeg-4.0-win64-static')

print("Done!")