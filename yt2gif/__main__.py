#!/usr/bin/env python3

import yt2gif
from argparse import ArgumentParser
from shutil import rmtree
from imp import load_source
from os import rename, path
from sys import argv

def parse_args():
    parser = ArgumentParser(description=
        'Turn a youtube video into a gif!')
    parser.add_argument('-s','--script',
        help='Python file that specifies a gif to create. See the "examples" folder.')
    parser.add_argument('-u','--url',
        help='Youtube url to download video from')
    parser.add_argument('-c','--cut',
        help='Time to cut the video down to. Formated as hh:mm:ss.x-hh:mm:ss.x')
    parser.add_argument('-o','--name', default="final",
        help='File to save the final gif as')
    parser.add_argument('--crop', action='store_true',
        help='Crop the gif to wide screen cinema')  
    parser.add_argument('--cleanup', action='store_true',
        help='Delete all files in the temp directory. Other arguments ignored.') 
    return parser.parse_args()

def main():
    if len(argv) == 1:
        argv.append('-h')
    opts = parse_args()
    
    if opts.cleanup:
        rmtree('/'.join(yt2gif.td.split('/')[:-1]))
        return
    
    if not opts.url:
        global data
        with open(opts.script) as fh:
            data = load_source('data','',fh)

        yt2gif.download_yt(data.url)
        yt2gif.make_cuts(data.cuttimes, opts.crop)
        data.build()
        yt2gif.concat_scenes( data.concatenate_order )        
        yt2gif.subVideo(data.subs,inputvid=yt2gif.concat_file,outputvid=opts.name+'.avi')
        
    else:
        yt2gif.download_yt(opts.url)
        yt2gif.make_cuts([tuple(opts.cut.split('-'))], opts.crop)
        rename(path.join(yt2gif.td,'cut1.avi'), opts.name+'.avi')
        
    yt2gif.gif_that(opts.name)
    yt2gif.cleanup()
    
if __name__ == "__main__":
    main()
