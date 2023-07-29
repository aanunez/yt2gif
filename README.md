# yt2gif
Downloads a youtube video and turns it into a gif. By writing a short python script subtitles and scenes (in any order) can be added.

A gernalized version of [this](https://github.com/1-Sisyphe/youCanCodeAGif) project. 

#### Dependencies 

You can either use `pipenv` to install the requirments in a virtual env or install with...

    pip3 install numpy pillow
	
You will also need `ffmpeg` and `youtube-dl`, they ship with most modern linux distros, or are in the repos.

On Windows you can either manually download them and place them in the calling directory or run the provided `win_dl.py` script.

#### Examples

For script examples check the examples folder.

Create a rick and morty gif from RTJ's Oh Mama

    python3 -m yt2gif -u "https://www.youtube.com/watch?v=EBYsx1QWF9A" -c 00:01:53.0-00:01:54.2
    
Or a gif of Awkwafina (a rapper) getting punched by her cat

    python3 -m yt2gif -u "https://www.youtube.com/watch?v=0-taYShNaPU" -c 00:02:52.0-00:02:53.8

![Cool Cat](https://raw.githubusercontent.com/aanunez/yt2gif/master/gifs/awkwafina.gif)

#### Bugs/todo

* Make more scripts, find more bugs.
* Finish that gif for my friend jessie
