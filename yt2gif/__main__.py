#!/usr/bin/env python3

import yt2gif
import os
import sys
import imp
import shutil
import argparse
import subprocess

def check_dependencies():
    flag = True
    if os.name == 'nt':
        if not os.path.isfile('ffmpeg.exe') or not os.path.isfile('youtube-dl.exe'):
            print('Please run the win_dl.py script to grab ffmpeg and youtube-dl')
    else:
        try:
            subprocess.call(['youtube-dl'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print('Please install youtube-dl')
                flag = False
            else:
                raise
        try:
            subprocess.call(['ffmpeg'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print('Please install ffmpeg')
                flag = False
            else:
                raise
    return flag

def parse_args():
    parser = argparse.ArgumentParser(description=
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
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    opts = parse_args()
    
    if opts.cleanup:
        shutil.rmtree('/'.join(yt2gif.td.split('/')[:-1]))
        return
    
    if os.name !='nt':
        if not check_dependencies():
            raise SystemExit
    
    if not opts.url:
        global data
        with open(opts.script) as fh:
            data = imp.load_source('data','',fh)

        yt2gif.download_yt(data.url)
        yt2gif.make_cuts(data.cuttimes, opts.crop)
        data.build()
        yt2gif.concatScenes( data.concatenate_order )        
        yt2gif.subVideo(data.subs,inputvid=yt2gif.concat_file,outputvid=opts.name+'.avi')
        
    else:
        yt2gif.download_yt(opts.url)
        yt2gif.make_cuts([tuple(opts.cut.split('-'))], opts.crop)
        os.rename(os.path.join(yt2gif.td,'cut1.avi'), opts.name+'.avi')
        
    yt2gif.gif_that(opts.name)
    yt2gif.cleanup()
    
if __name__ == "__main__":
    main()
