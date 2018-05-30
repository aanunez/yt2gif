#!/usr/bin/env python3

import yt2gif

url = 'https://www.youtube.com/watch?v=viP_aYOSecU'
cuttimes =[
    ("00:04:15.5","00:04:18.0")
]

subs =[]

concatenate_order =[
    "cut1.avi"
]

def build():
    yt2gif.makeVideo(seqname="cut1")
