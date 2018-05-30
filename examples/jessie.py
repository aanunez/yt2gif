#!/usr/bin/env python3

import yt2gif

url = 'https://www.youtube.com/watch?v=TS_59Y7bYoA'
cuttimes =[
    ("00:00:40.5","00:00:57.0"),
    ("00:01:00.7","00:01:04.5"),
    ("00:01:13.5","00:01:15.2"),
    ("00:01:20.3","00:01:31.5"),
    ("00:01:38.8","00:01:40.9"),
    ("00:01:47.2","00:01:48.3"),
    ("00:01:50.6","00:01:53.3"),
    ("00:01:55.9","00:02:00.0"),
    ("00:00:27.0","00:00:27.1")
]

Crop = True
    
white=(255,255,255)
yellow=(255,233,155)
subs =[
    ["What are you working on?",yellow,(830,420),'1,2.5'],
    ["A Poem for Jessie",white,(800,420),'3,4'],
    ["I forgot to write one",white,(800,420),'4.1,7'],
    ["and I've been putting it off",white,(800,480),'5.2,7'],
    ["This doesn't look like a poem",yellow,(800,450),'7.1,10'],
    ["Of course not",white,(820,420),'11.8,13'],
    ["It's a gif of me writting the poem",white,(800,420),'14,16'],
    ["So what have you got?",yellow,(800,480),'15,16'],
    ["Not much...",white,(640,450),'17,19.5'],
    # Cut to screen with crappy poem
    ["I think it needs some work",yellow,(640,480),'20,23'],
    ["She likes cute stuff",yellow,(640,480),'24,25.4'],
    ["how about you just get her a candle?",yellow,(640,480),'30.5,32.5'],
    # Cut back to dude talking
    ["I already did that",white,(640,480),'32.9,34.5'],
    ["how about this...",white,(640,420),'35,40'],
    # Cut back to screen, display happy B-day message
    ["oh, she might like that",yellow,(640,480),'37,40'],
    ["its not a poem, but I hope she likes it",white,(640,480),'45.6,47.6'],
]

concatenate_order =[
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
]

bday = """
                   H    H   A       PPPP    PPPP   Y     Y
                  H    H   A A     P    P  P    P   Y   Y
                 HHHHHH   A  A    PPPPPP  PPPPPP     YYY
                H    H   AAAAA   P       P            Y
               H    H   A    A  P       P            Y

                                        /
                                /      +       /
                         /     +       W      +
                        +      W       I      W
                    /   W      I       S      I
                   +    I BBBB S BBBBB H BBBB S
                   W B' S UU ' H UUU'U E UUU' H BBB /
              BBB' I 'O H U /U E UUUUU S UUUU E U' + BB
           BBBB''U S UU E  + U S UUUUUUUUUUUU S UU W 'BBBB
          BBB''UUU H UU S  W UUUUUUUUUUUUUUUUUUUUU I UU''BBB
         BBB''UUUU E UUUUU I UUUUUUUUUUUUUUUUUUUUU S UUU''BB
         BBBB''UUU S UUUUU S UUU ''''''''''''''''' H ''''''B
         BBBBB''UUUUUUUUUU H UUUU ///UUUUUUUUUUUUU E UUUUUUUU''BB
         BBBBBB''UUUUUUUUU E UUUUUU ///UUUUUUUUUUU S UUUUUUU''BBBB
         BBBBBBBB''UUUUUUU S UUUUUUUU ///UUUUUUUUUUUUUUUUUUU''BBBBB
         BBBBBBBBBBBB''UUUUUUUUUUUUUUUU ///UUUUUUUUUUUUUUU''BBBBBBB
         + BBBBBBBBBBBBBB''UUUUUUUUUUUUUU ///UUUUUUUUUUU''BBBBBBBBB
         BBBBBBBB + BBBBBBBBBBBBBBBB''UUUU  ////'UUU''BBBBBBBBB + BB
         BBBBBBB + + BBBBBBBBBBBBBBBBBBBBBB  ///BBBBBBBBBBBBBB + + B
         BBBBBB + + + BBBBBBBBBBBBBBBBBBBBB  ///BBBBBBBBBBBBB + + +B
         BBBBBBB + + BBBBBBBB + BBBBBBBBBBB  ///BBBBBBBBBBBBBB + + B
         BBBBBBBB + BBBBBBBB + + BBBBBBBBBB  ///BBB + BBBBBBBBB + BB
         BBBBBBBBBBBBBBBBBB + + + BBBBBBBBB  ///BB + + BBBBBBBBBBBBB
        +BBBBBBBBBBBBBBBBBBB + + BBBBBBBBBB  ///B + + + BBBBBBBBBBB +
         +BBBBBBBBBBBBBBBBBBB + BBBBBBBBBBB  ///BB + + BBBBBBBBBBB +
          +BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB  ///BBB + BBBBBBBBBBB +
            +BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB  ///BBBBBBBBBBBBBBBB +
               + BBBBBBBBBBBBBBBBBBBBBBBBBB  ///BBBBBBBBBBBBBB +
                    +  BBBBBBBBBBBBBBBBBBBB  ///BBBBBBBBBBBB +
                         +   BBBBBBBBBBBBBB  ///BBBBBBBB  +
                               +   BBBBBBBB  ///BBBB  +

        RRRRR    I    RRRRR   TTTTTT   H    H   RRRR      A   Y     Y
       R   R    I    R     R    T     H    H   R    R    A A   Y   Y
      RRRR     I    RRRRRRR    T     HHHHHH   R     R   A  A    YYY
     R    R   I    R   R      T     H    H   R    R    AAAAA     Y
    RRRRRR   I    R     R    T     H    H   RRRRR     A    A    Y"""

def build():
    #take a snapshot used as background for the terminal
    yt2gif.snapshotBackground('temp/cut9.avi')
    #open this code as a string
    script_lines = [line.rstrip('\n') for line in open('examples/YouCanCodeAGif.py')]
    #youtube-dl terminal scene
    code_dlvideo_1 = '\n'.join(script_lines[45:54])
    code_dlvideo_2 = '\n'.join(script_lines[45:54])
    code_dlvideo_3 = '\n'.join(script_lines[45:54])
    textcuts = yt2gif.cutText(code_dlvideo_1,method='char',randfactors=(1,3),repeatlast=10)
    textcuts += yt2gif.cutText(code_dlvideo_2,starttext=code_dlvideo_1+'\n',
                                  method='line',randfactors=(1,1),slowfactor=2,repeatlast=10)
    textcuts += yt2gif.cutText(code_dlvideo_3,starttext=code_dlvideo_1+'\n'+code_dlvideo_2+'\n',
                                  method='char',randfactors=(1,3),repeatlast=24)
    yt2gif.drawFrames(seqname="dlvideo", textcuts=textcuts)
    yt2gif.makeVideo(seqname="dlvideo")

    #add subtitles scene
    code_subs = '\n'.join(script_lines[45:54])
    textcuts = yt2gif.cutText(code_subs,method='line',slowfactor=3,repeatlast=24,typingchar='')
    yt2gif.drawFrames(seqname="subs", textcuts=textcuts, fontsize=15)
    yt2gif.makeVideo(seqname="subs")

    #add concat scene
    code_concat = '\n'.join(script_lines[45:54])
    textcuts = yt2gif.cutText(code_concat,method='line',slowfactor=4,repeatlast=24,typingchar='')
    yt2gif.drawFrames(seqname="concat", textcuts=textcuts, fontsize=16)
    yt2gif.makeVideo(seqname="concat")

    #add gifthat scene
    code_gif_that = '\n'.join(script_lines[45:54])
    textcuts = yt2gif.cutText(code_gif_that,method='char',randfactors=(1,3),repeatlast=24)
    yt2gif.drawFrames(seqname="gifthat", textcuts=textcuts, fontsize=16)
    yt2gif.makeVideo(seqname="gifthat")

    #add blackscreen scene
    empty_screen = """\n\n"""
    textcuts = yt2gif.cutText(empty_screen,method='char',randfactors=(1,1),repeatlast=24,typingchar='')
    yt2gif.drawFrames(seqname="empty_screen", textcuts=textcuts, fontsize=16)
    yt2gif.makeVideo(seqname="empty_screen")

    #add "add a touch meta" scene
    code_add_meta = '\n'.join(script_lines[45:54])
    textcuts = yt2gif.cutText(code_add_meta,method='line',slowfactor=6,repeatlast=24,typingchar='')
    yt2gif.drawFrames(seqname="add_meta", textcuts=textcuts)
    yt2gif.makeVideo(seqname="add_meta")

    #add a touch of meta
    meta_cuts = yt2gif.cutText(bday,method='line',
            slowfactor=1,repeatlast=10,typingchar='')
    yt2gif.drawFrames(seqname="meta",
                    textcuts=meta_cuts,fontsize=14)
    yt2gif.makeVideo(seqname="meta")

