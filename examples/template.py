#!/usr/bin/env python3

import yt2gif

url = 'Some youtube url here'

# Set to true to crop to extra wide for that ciema effect
crop = False

# You must specify atleast one cut time
cuttimes =[
    ("00:00:30.5","00:00:35.0")
]
    
# You must define the sub-title array 
subs =[]

# You must include atleast one scene in the concat list
concatenate_order =[
    "cut1.avi"
]

# You must invoke makevideo atleast once in your build function
def build():
    yt2gif.makeVideo(seqname="cut1")
