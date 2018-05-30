#!/usr/bin/env python3

import yt2gif
from argparse import ArgumentParser
from importlib import import_module
from imp import load_source

def parse_args():
    parser = ArgumentParser(description=
        'Turn a youtube video into a gif!')
        
    parser.add_argument('input', nargs='?', default="examples/YouCanCodeAGif.py",
        help='input')

    return parser.parse_args()

def main():
    opts = parse_args()

    global data
    with open(opts.input) as fh:
        data = load_source('data', '', fh)

    yt2gif.make_temp()
    yt2gif.download_yt(data.url)
    yt2gif.make_cuts(data.cuttimes)
    data.build()
    yt2gif.concat_scenes( data.concatenate_order )        
    yt2gif.subVideo(data.subs,inputvid='temp/concat_nosub.avi',outputvid='final.avi')
    yt2gif.gif_that()
    yt2gif.del_temp()
    
if __name__ == "__main__":
    main()
