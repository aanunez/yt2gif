#!/usr/bin/env python3

import os
import data
import numpy
from shutil import rmtree
from random import randint
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def make_temp():
    if not os.path.exists('temp'):
        os.makedirs('temp')
        
    if os.path.exists('temp/sub/'):
        rmtree('temp/sub/')
    os.makedirs('temp/sub/')

    if os.path.exists('temp/frames/'):
        rmtree('temp/frames/')
    os.makedirs('temp/frames/')
    
def del_temp():
    rmtree('temp/')

def download_yt( url ):
    os.system(r'youtube-dl -f 136 -o temp/in.mp4 ' + url)


def make_cuts( cutlist ):
    n = 1
    cuts=[]
    for cut in cutlist:
        outvid = 'temp/cut' + str(n) + '.avi'
        cuts.append(outvid)
        n += 1
        print( "Cutting scene " + str(n) )
        os.system( "ffmpeg -i temp/in.mp4 -ss " + cut[0] +
            ' -filter:v "crop=1280:540:0:90" -c:v ffv1' +
            " -to "+ cut[1] + " -r 24 -y " + outvid)
            
       
def makePngSub(text, color, position, filename):
    """"Turn a text into a png"""
    img = Image.new('RGBA',(1280, 544))
    x,y = position
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Ubuntu-B.ttf",60)
    w, h = draw.multiline_textsize(text, font=font)
    x = x - w/2
    y = y - h/2
    for i in range(1,6):
        draw.multiline_text((x+i,y+i), text, fill=(0,0,0), font=font, align='center')
    draw.multiline_text((x,y), text, fill=color, font=font, align='center')
    filename = 'temp/sub/{}.png'.format(filename)
    img.save(filename, 'PNG')
    return filename


def subVideo(subs,inputvid,outputvid):
    """Take a list a subtitles, make each png with makePngSub()
    and add the pngs to the video at the given intervals"""
    n=1
    subfiles=[]
    for sub in subs:
        subfile = makePngSub(text=sub[0],color=sub[1],position=sub[2],filename=str(n))
        subfiles.append(subfile)
        n+=1

    def writeFilterblocks(subs):
        """write the complex filter to chain-add all the png in one shot"""
        n = 0
        filter_blocks=[]
        for sub in subs:
            timing = sub[3]
            blocks=['']*4
            if n==0:
                blocks[0]='"[0:v]'
            else:
                blocks[0]='[tmp]'
            n+=1
            blocks[1]='['+str(n)+':v]'
            blocks[2]="overlay=enable='between(t,{})'".format(timing)
            if n!=len(subs):
                blocks[3]=' [tmp]; '
            else:
                blocks[3]='"'
            filter_blocks+=blocks
        return filter_blocks

    inputblocks = ['ffmpeg -i '+inputvid]+['-i '+subfile for subfile in subfiles]
    inputstr = ' '.join(inputblocks)
    filterstr = '-filter_complex '+''.join(writeFilterblocks(subs))
    #outputstr = '-y '+ outputvid
    outputstr = '-y -c:v ffv1 '+ outputvid
    command = inputstr+' '+filterstr+' '+outputstr
    os.system(command)


def snapshotBackground(cutscene):
    """Take a 1-frame shot from the video, used as background for the terminal"""
    command='ffmpeg -ss 00:00:00 -i {} -vf "select=eq(n\,0)" -q:v 1 -y temp/background.png'.format(cutscene)
    os.system(command)


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

    font_title = ImageFont.truetype("fonts/COURIER.TTF",15)
    font_text = ImageFont.truetype("fonts/COURIER.TTF",fontsize)
    img=Image.new("RGBA", (x,y),black)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((4,4),(x-5,y-5)), outline = light)
    draw.rectangle(((5,5),(x-5,y-5)), outline = white)
    draw.rectangle(((9,9),(x-10,30)), outline = light)
    draw.rectangle(((10,10),(x-10,30)), outline = white)

    draw.text((11, 15),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',light,
              font=font_title)
    draw.text((12, 16),'  GIFOLATINE 3000 V1.337 - By 1-Sisyphe',white,
              font=font_title)
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
    img_finale = Image.open('temp/background.png')
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
    for n in range(len(textcuts)):
        cut = textcuts[n]
        if cut == '': cut = ' '
        cut = cut.replace('\n',' \n ')
        img = drawTerminal(cut, fontsize)
        img.save('temp/frames/'+seqname+str(n).zfill(4)+'.png')
        n += 1


def makeVideo(seqname, framerate='24', r='24'):
    """Take all seqname png and join them in an AVI video."""
    os.system('ffmpeg -framerate '+framerate
              +' -i temp/frames/'+seqname+'%04d.png'
              +' -c:v ffv1'+' -r '+r+' -pix_fmt yuv420p -y '
              +'temp/'+seqname+'.avi')
              
def gif_that():
    os.system('ffmpeg -y -i final.avi -vf fps=24,scale=1080:-1:'+
              'flags=lanczos,palettegen temp/palette.png')
    os.system('ffmpeg  -i final.avi -i temp/palette.png -filter_complex '+
              '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+
              'you_can_code_a.gif')

def concat_scenes( concat_order ):
    with open('temp/list.txt','w') as f:
        for vid in concat_order:
            print("file '"+vid+"'",file=f)
    os.system('ffmpeg -f concat -i temp/list.txt -c copy -y temp/concat_nosub.avi')
