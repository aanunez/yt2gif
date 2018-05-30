#!/usr/bin/env python3

import yt2gif

url = 'https://www.youtube.com/watch?v=HcXMahu7q-k'
cuttimes =[
    ("00:00:02.5","00:00:10.0")
]
    

subs =[]

concatenate_order =[
    "cut1.avi"
]

def build():
    yt2gif.makeVideo(seqname="cut1")
