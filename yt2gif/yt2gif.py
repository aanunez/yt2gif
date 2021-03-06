#!/usr/bin/env python3

import os
import numpy
from shutil import rmtree
from random import randint
from PIL import Image, ImageFont, ImageDraw
from tempfile import gettempdir
from datetime import datetime

# Deal with windows sucking
ffmpeg = 'ffmpeg' if os.name != 'nt' else 'yt2gif\\win\\ffmpeg.exe'
ytdl = 'youtube-dl' if os.name != 'nt' else 'yt2gif\\win\\youtube-dl.exe'

# Temp directory 
td = os.path.join(gettempdir(),'yt2gif',
	str(datetime.now()).split('.')[0].replace(' ','.').replace(':','.'))
sub_dir = os.path.join(td,'sub')
os.makedirs(sub_dir)
frames_dir = os.path.join(td,'frames')
os.makedirs(frames_dir)

# Temp files that will be used
ubuntu_font = os.path.join('yt2gif','fonts','Ubuntu-B.ttf')
courier_font = os.path.join('yt2gif','fonts','COURIER.TTF')
palette_file = os.path.join(td,'palette.png')
list_file = os.path.join(td,'list.txt')
concat_file = os.path.join(td,'concat_nosub.avi')
in_file = os.path.join(td,'in.mp4')
background_file = os.path.join(td,'background.png')

# Basic functions
cleanup     = lambda     : rmtree(td)
download_yt = lambda url : os.system(ytdl+' -f 136 -o ' + in_file + ' ' + url)

def snapshot(cutscene):
    os.system(ffmpeg+' -ss 00:00:00 -i '+cutscene+' -vf "select=eq(n\,0)" -q:v 1 -y '+background_file)
    
def concatScenes(concat_order):
    os.system(ffmpeg+' -i "concat:'+'|'.join([os.path.join(td,L) for L in concat_order])+'" -c copy -y ' + concat_file)

def make_cuts(cutlist, cinemaCrop=False):
    crop = ' -filter:v "crop=1280:540:0:90"' if cinemaCrop else ''
    cuts=[]
    for n,cut in enumerate(cutlist,1):
        outvid = os.path.join(td,'cut'+str(n)+'.avi')
        cuts.append(outvid)
        print( 'Cutting scene ' + str(n+1) )
        os.system(ffmpeg+' -i '+ in_file + ' -ss ' + cut[0] + crop + ' -c:v ffv1' +
            ' -to '+ cut[1] + ' -r 24 -y ' + outvid)

def gif_that(name):
    os.system(ffmpeg+' -y -i final.avi -vf fps=24,scale=1080:-1:'+'flags=lanczos,palettegen '+palette_file)
    os.system(ffmpeg+'  -i final.avi -i ' + palette_file + ' -filter_complex '+
              '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+name+ '.gif')
     
# The follow are only used when making a gif with subs or fancy terminal drawing     
def makeVideo(seqname, framerate='24', r='24'):
    os.system(ffmpeg+' -framerate '+framerate+' -i ' + os.path.join(frames_dir,seqname+'%04d.png')
              +' -c:v ffv1'+' -r '+r+' -pix_fmt yuv420p -y '+os.path.join(td,seqname+'.avi'))
  
def subVideo(subs,inputvid,outputvid):
    """Take a list a subtitles, make each png with makePngSub()
    and add the pngs to the video at the given intervals"""
    if not subs:
        os.rename(inputvid, outputvid)
        return 
        
    def makePngSub(text, color, position, filename):
        """"Turn a text into a png"""
        img  = Image.new('RGBA',(1280, 544))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(ubuntu_font,60)
        w, h = draw.multiline_textsize(text, font=font)
        x, y = position[0] - w/2, position[1] - h/2
        for i in range(1,6):
            draw.multiline_text((x+i,y+i), text, fill=(0,0,0), font=font, align='center')
        draw.multiline_text((x,y), text, fill=color, font=font, align='center')
        img.save(os.path.join(sub_dir,filename+'.png'), 'PNG')
        return filename

    def writeFilterblocks(subs):
        """write the complex filter to chain-add all the png in one shot"""
        filter_blocks=[]
        for n,sub in enumerate(subs):
            timing = sub[3]
            blocks=['']*4
            blocks[0] = '"[0:v]' if n==0 else '[tmp]'
            blocks[1] = '['+str(n+1)+':v]'
            blocks[2] = "overlay=enable='between(t,{})'".format(timing)
            blocks[3] = ' [tmp]; ' if (n+1)!=len(subs) else '"'
            filter_blocks+=blocks
        return filter_blocks
     
    subfiles=[]
    for n,sub in enumerate(subs,1):
        subfile = makePngSub(text=sub[0],color=sub[1],position=sub[2],filename=str(n))
        subfiles.append(subfile)

    inputblocks = ''.join([' -i '+os.path.join(sub_dir,subfile+'.png') for subfile in subfiles])
    filterstr = '-filter_complex '+''.join(writeFilterblocks(subs))
    os.system(ffmpeg+' -i '+ inputvid + inputblocks + ' ' + filterstr + ' -y -c:v ffv1 '+ outputvid)

def drawTerminal(text, fontsize):
    """Compose an img made of a pseudo-terminal interface,
    with print outs of text and a background from the main video"""
    black = (16,16,16)
    light = (150,210,150)
    white = (190,210,230)
    x,y=(695,500)

    font_title = ImageFont.truetype(courier_font,15)
    font_text = ImageFont.truetype(courier_font,fontsize)
    img=Image.new("RGBA", (x,y),black)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((4,4),(x-5,y-5)),   outline = light)
    draw.rectangle(((5,5),(x-5,y-5)),   outline = white)
    draw.rectangle(((9,9),(x-10,30)),   outline = light)
    draw.rectangle(((10,10),(x-10,30)), outline = white)

    draw.text((11, 15),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',light, font=font_title)
    draw.text((12, 16),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',white, font=font_title)
    draw.text((x-50, 15),'X O',white,font=font_title)

    draw.multiline_text((10, 40),text,light,font=font_text)
    draw.multiline_text((11, 41),text,white,font=font_text)

    new_size = (800, 800)
    new_im = Image.new("RGBA", new_size)
    new_im.paste(img,(0,100))

    def find_coeffs(pa, pb):
        """used in drawTerminal to deform terminal's perspective"""
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(pb).reshape(8)

        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    coeffs = find_coeffs(
        [(0, 0), (x, 0), (x, y), (0, y)],
        [(0, 0), (x, 50), (x, 450), (0, y)])

    img = new_im.transform(new_size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    img = img.rotate(0.5, resample=Image.BICUBIC)
    img_finale = Image.open(background_file)
    img_finale.paste(img,(340,-75),img)

    return img_finale

def cutText(text,starttext='',maxframes=None,method='char',
            randfactors=(1,1),slowfactor=1, typingchar='[]',
            repeatlast=0):
    """Take a text and cut it in a list of strings, used to animate the
    terminal frame by frame via drawFrames()"""
    cuts=[]
    n = 1
    if method == 'line':
        text = text.split('\n')
    while n < len(text):
        if method == 'line':
            cut = '\n'.join(text[:n])
        else:
            cut = text[:n]
        for r in range(1,slowfactor+1):
            cuts.append(cut)
        n += randint(*randfactors)
    if not maxframes:
        maxframes=len(cuts)+repeatlast
    cuts = cuts[:maxframes-repeatlast]
    for r in range(repeatlast):
        cuts.append(cuts[-1])

    cuts=[starttext+cut+typingchar for cut in cuts]
    return cuts

def drawFrames(seqname, textcuts, fontsize=16):
    """Pass each item of the textcuts list into drawTerminal() and
    save the result as a png in temp/frames, with an incremental filename
    starting by seqname."""
    for n,tc in enumerate(textcuts):
        cut = ' ' if tc == '' else tc.replace('\n',' \n ')
        img = drawTerminal(cut, fontsize)
        img.save(os.path.join(frames_dir,seqname+str(n).zfill(4))+'.png')

