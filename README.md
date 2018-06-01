# yt2gif
Downloads a youtube video, turns it into a gif with optional subtitles.

Based on [this](https://github.com/1-Sisyphe/youCanCodeAGif). WIP. Lots of the code is still under their MIT license, but I'm expecting to eventually overhaul everything. 

#### Dependencies 

You can either use `pipenv` to install the requirments in a virtual env or install with...

    pip3 install numpy pillow
	
You will also need `ffmpeg` and `youtube-dl`, they ship with most modern linux distros, or are in the repos.

On Windows you can either manually download them and place them in the calling directory or run the provided `win_dl.py` script.

#### Examples

Create a rick and morty gif from RTJ's Oh Mama

    python3 -m yt2gif -u "https://www.youtube.com/watch?v=EBYsx1QWF9A" -c 00:01:53.0-00:01:54.2
    
Or a gif of Awkwafina (a rapper) getting punched by her car

    python3 -m yt2gif -u "https://www.youtube.com/watch?v=0-taYShNaPU" -c 00:02:52.0-00:02:53.8

![Cool Cat](https://raw.githubusercontent.com/aanunez/yt2gif/master/gifs/awkwafina.gif)

#### Bugs/todo

* Finish that gif for my friend jessie
* General clean up of yt2gif
* Let scripts define real crop patterns and not just 'cinema'
