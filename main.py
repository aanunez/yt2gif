#!/usr/bin/env python3

import os
import data
import numpy
from shutil import rmtree
from random import randint
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

if not os.path.exists('temp'):
    os.makedirs('temp')
if os.path.exists('temp/sub/'):
    shutil.rmtree('temp/sub/')
os.makedirs('temp/sub/')
if os.path.exists('temp/frames/'):
    shutil.rmtree('temp/frames/')
os.makedirs('temp/frames/')
if os.path.exists('temp/log'):
    os.remove('temp/log')
   
#temp destinations 
input_video = 'temp/in.mp4'
temp_folder = 'temp/'
logfile = 'temp/log'

def download_yt( url ):
    os.system(r'youtube-dl -f 136 -o ' + input_video + ' ' + url)


def make_cuts( cutlist ):
    n = 1
    cuts=[]
    for cut in cutlist:
        outvid = temp_folder + 'cut' + str(n) + '.avi'
        cuts.append(outvid)
        n += 1
        print( "Cutting scene " + str(n) )
        os.system( "ffmpeg -i " + input_video + " -ss " + cut[0] +
            ' -filter:v "crop=1280:540:0:90"' + " -c:v ffv1" +
            " -to "+ cut[1] + ' -r 24 -y ' + outvid + '>> ' + logfile)
            
       
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
        n += random.randint(*randfactors)
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
              +' -c:v ffv1'
              +' -r '+r
              +' -pix_fmt yuv420p -y '
              +'temp/'+seqname+'.avi')

download_yt(data.url)
make_cuts( data.cuttimes)

#create the terminal scenes
#take a snapshot used as background for the terminal
snapshotBackground('temp/cut9.avi')
#open this code as a string
script_lines = [line.rstrip('\n') for line in open('data.py')]
#youtube-dl terminal scene
code_dlvideo_1 = '\n'.join(script_lines[45:54])
code_dlvideo_2 = '\n'.join(script_lines[45:54])
code_dlvideo_3 = '\n'.join(script_lines[45:54])
textcuts = cutText(code_dlvideo_1,method='char',randfactors=(1,3),repeatlast=10)
textcuts += cutText(code_dlvideo_2,starttext=code_dlvideo_1+'\n',
                              method='line',randfactors=(1,1),slowfactor=2,repeatlast=10)
textcuts += cutText(code_dlvideo_3,starttext=code_dlvideo_1+'\n'+code_dlvideo_2+'\n',
                              method='char',randfactors=(1,3),repeatlast=24)
drawFrames(seqname="dlvideo", textcuts=textcuts)
makeVideo(seqname="dlvideo")

#add subtitles scene
code_subs = '\n'.join(script_lines[45:54])
textcuts = cutText(code_subs,method='line',slowfactor=3,repeatlast=24,typingchar='')
drawFrames(seqname="subs", textcuts=textcuts, fontsize=15)
makeVideo(seqname="subs")

#add concat scene
code_concat = '\n'.join(script_lines[45:54])
textcuts = cutText(code_concat,method='line',slowfactor=4,repeatlast=24,typingchar='')
drawFrames(seqname="concat", textcuts=textcuts, fontsize=16)
makeVideo(seqname="concat")

#add gifthat scene
code_gif_that = '\n'.join(script_lines[45:54])
textcuts = cutText(code_gif_that,method='char',randfactors=(1,3),repeatlast=24)
drawFrames(seqname="gifthat", textcuts=textcuts, fontsize=16)
makeVideo(seqname="gifthat")

#add blackscreen scene
empty_screen = """\n\n"""
textcuts = cutText(empty_screen,method='char',randfactors=(1,1),repeatlast=24,typingchar='')
drawFrames(seqname="empty_screen", textcuts=textcuts, fontsize=16)
makeVideo(seqname="empty_screen")

#add "add a touch meta" scene
code_add_meta = '\n'.join(script_lines[45:54])
textcuts = cutText(code_add_meta,method='line',slowfactor=6,repeatlast=24,typingchar='')
drawFrames(seqname="add_meta", textcuts=textcuts)
makeVideo(seqname="add_meta")

#add a touch of meta
meta_cuts = cutText(data.dickbutt,method='line',
        slowfactor=1,repeatlast=10,typingchar='')
drawFrames(seqname="meta",
                textcuts=meta_cuts,fontsize=14)
makeVideo(seqname="meta")

#concatenate the scenes
to_concat =[
    "cut1.avi",
    "dlvideo.avi",
    "cut5.avi",
    "subs.avi",
    "cut4.avi",
    "add_meta.avi",
    "cut3.avi",
    "concat.avi",
    "cut7.avi",
    "gifthat.avi",
    "empty_screen.avi",
    "meta.avi",
    "cut8.avi"
]
with open('temp/list.txt','w') as f:
    for vid in to_concat:
        print("file '"+vid+"'",file=f)
os.system('ffmpeg -f concat -i temp/list.txt'+
          ' -c copy -y temp/concat_nosub.avi >> ' + logfile)

#add the subtitles
subVideo(data.subs,inputvid='temp/concat_nosub.avi',outputvid='final.avi')

#gif THAT
os.system('ffmpeg -y -i '+
          'final.avi -vf '+
          'fps=24,scale=1080:-1:'+
          'flags=lanczos,palettegen temp/palette.png >> ' + logfile)

os.system('ffmpeg  -i final.avi '+
          '-i temp/palette.png -filter_complex '+
          '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse" '+
          'you_can_code_a.gif >> ' + logfile)
