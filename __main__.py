#!/usr/bin/env python3

import yt2gif
import data

def __main__():
    yt2gif.download_yt(data.url)
    yt2gif.make_cuts(data.cuttimes)
    data.build()
    yt2gif.concat_scenes( data.concatenate_order )        
    yt2gif.subVideo(data.subs,inputvid='temp/concat_nosub.avi',outputvid='final.avi')
    yt2gif.gif_that()
    
__main__()
