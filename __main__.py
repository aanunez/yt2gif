#!/usr/bin/env python3

import yt2gif
import data
from argparse import ArgumentParser, ArgumentTypeError

def parse_args():
    parser = ArgumentParser(description=
        'Explanation here.')
        
    parser.add_argument('-o','--output', default=None, help=
        'Input file')

    return parser.parse_args()

def __main__():
    yt2gif.make_temp()
    yt2gif.download_yt(data.url)
    yt2gif.make_cuts(data.cuttimes)
    data.build()
    yt2gif.concat_scenes( data.concatenate_order )        
    yt2gif.subVideo(data.subs,inputvid='temp/concat_nosub.avi',outputvid='final.avi')
    yt2gif.gif_that()
    yt2gif.del_temp()
    
__main__()
