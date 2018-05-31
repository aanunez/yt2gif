#!/usr/bin/env python3

import os
import numpy
from shutil import rmtree
from random import randint
from PIL import Image, ImageFont, ImageDraw
from tempfile import gettempdir

td = gettempdir() + '/yt2gif'
os.makedirs(td + '/sub/')
os.makedirs(td + '/frames/')	

cleanup     = lambda     : rmtree(td)
download_yt = lambda url : os.system(r'youtube-dl -f 136 -o '+ td +'/in.mp4 ' + url)

def make_cuts(cutlist, cinemaCrop=False):
    crop = ' -filter:v "crop=1280:540:0:90"' if cinemaCrop else ''
    cuts=[]
    for n,cut in enumerate(cutlist,1):
        outvid = td + '/cut' + str(n) + '.avi'
        cuts.append(outvid)
        print( 'Cutting scene ' + str(n+1) )
        os.system( 'ffmpeg -i '+ td +'/in.mp4 -ss ' + cut[0] + crop + ' -c:v ffv1' +
            ' -to '+ cut[1] + ' -r 24 -y ' + outvid)
            
       
def makePngSub(text, color, position, filename):
    """"Turn a text into a png"""
    img  = Image.new('RGBA',(1280, 544))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf",60)
    w, h = draw.multiline_textsize(text, font=font)
    x, y = position[0] - w/2, position[1] - h/2
    for i in range(1,6):
        draw.multiline_text((x+i,y+i), text, fill=(0,0,0), font=font, align='center')
    draw.multiline_text((x,y), text, fill=color, font=font, align='center')
    img.save(td + '/sub/'+filename+'.png', 'PNG')
    return filename


def subVideo(subs,inputvid,outputvid):
    """Take a list a subtitles, make each png with makePngSub()
    and add the pngs to the video at the given intervals"""
    if not subs:
        os.rename(inputvid, outputvid)
        return 
    subfiles=[]
    for n,sub in enumerate(subs,1):
        subfile = makePngSub(text=sub[0],color=sub[1],position=sub[2],filename=str(n))
        subfiles.append(subfile)

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

    inputblocks = ['ffmpeg -i '+inputvid]+['-i '+subfile for subfile in subfiles]
    filterstr = '-filter_complex '+''.join(writeFilterblocks(subs))
    os.system(' '.join(inputblocks) + ' ' + filterstr + ' -y -c:v ffv1 '+ outputvid)


def snapshotBackground(cutscene):
    """Take a 1-frame shot from the video, used as background for the terminal"""
    os.system('ffmpeg -ss 00:00:00 -i '+cutscene+' -vf "select=eq(n\,0)" -q:v 1 -y '+td+'/background.png')


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


def drawTerminal(text, fontsize):
    """Compose an img made of a pseudo-terminal interface,
    with print outs of text and a background from the main video"""
    black = (16,16,16)
    light = (150,210,150)
    white = (190,210,230)
    x,y=(695,500)

    font_title = ImageFont.truetype("yt2gif/fonts/COURIER.TTF",15)
    font_text = ImageFont.truetype("yt2gif/fonts/COURIER.TTF",fontsize)
    img=Image.new("RGBA", (x,y),black)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((4,4),(x-5,y-5)), outline = light)
    draw.rectangle(((5,5),(x-5,y-5)), outline = white)
    draw.rectangle(((9,9),(x-10,30)), outline = light)
    draw.rectangle(((10,10),(x-10,30)), outline = white)

    draw.text((11, 15),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',light, font=font_title)
    draw.text((12, 16),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',white, font=font_title)
    draw.text((x-50, 15),'X O',white,font=font_title)

    draw.multiline_text((10, 40),text,light,font=font_text)
    draw.multiline_text((11, 41),text,white,font=font_text)

    new_size = (800, 800)
    new_im = Image.new("RGBA", new_size)
    new_im.paste(img,(0,100))

    coeffs = find_coeffs(
        [(0, 0), (x, 0), (x, y), (0, y)],
        [(0, 0), (x, 50), (x, 450), (0, y)])

    img = new_im.transform(new_size, Image.PERSPECTIVE, coeffs,
        Image.BICUBIC)
    img = img.rotate(0.5, resample=Image.BICUBIC)
    img_finale = Image.open(td+'/background.png')
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
        img.save(td+'/frames/'+seqname+str(n).zfill(4)+'.png')

def makeVideo(seqname, framerate='24', r='24'):
    """Take all seqname png and join them in an AVI video."""
    os.system('ffmpeg -framerate '+framerate
              +' -i ' + td + '/frames/'+seqname+'%04d.png'
              +' -c:v ffv1'+' -r '+r+' -pix_fmt yuv420p -y '
              +td+'/'+seqname+'.avi')
              
def gif_that(name):
    os.system('ffmpeg -y -i final.avi -vf fps=24,scale=1080:-1:'+
              'flags=lanczos,palettegen ' + td + '/palette.png')
    os.system('ffmpeg  -i final.avi -i ' + td + '/palette.png -filter_complex '+
              '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+
              name + '.gif')

def concat_scenes( concat_order ):
    with open(td+'/list.txt','w') as f:
        for vid in concat_order:
            print("file '"+vid+"'",file=f)
    os.system('ffmpeg -f concat -i ' + td + '/list.txt -c copy -y ' + td + '/concat_nosub.avi')