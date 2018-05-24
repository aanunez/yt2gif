#!/usr/bin/env python3

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
    
white=(255,255,255)
yellow=(255,233,155)
subs =[
    ["You can't just code a gif...",yellow,(830,420),'1,2.5'],
    ["Of course I can.",white,(800,420),'3,4'],
    ["I'm going to code",white,(800,420),'4.1,7'],
    ["this entire gif.",white,(800,480),'5.2,7'],
    ["And I'll give you the\n source in the comments.",white,(800,450),'7.1,10'],
    ['"You can\'t code a gif..."',white,(820,420),'11.8,13'],
    ["It's nothing more than",white,(800,420),'14,16'],
    ["a huge waste of time!",white,(800,480),'15,16'],
    ["First: I download our video\nfrom Youtube.",white,(640,450),'17,19.5'],
    ["Then I separate each scene...",white,(640,480),'20,23'],
    ["Now I add our dialogs...",white,(640,480),'24,25.4'],
    ["Let me see...",yellow,(640,480),'30.5,32.5'],
    ["Can you add a bit of META?",yellow,(640,480),'32.9,34.5'],
    ["I will put just a touch...",white,(640,420),'35,40'],
    ["Very subtle, no one will see it.",white,(640,480),'37,40'],
    ["Now I concatenate the scenes....",white,(640,480),'45.6,47.6'],
    ["And to finish...",white,(640,420),'49.6,52'],
    ["GIF THAT!",white,(640,480),'50.2,52'],
    ["I AM",white,(640,400),'62.8,64.6'],
    ["INVINCIBLE!!!",white,(640,460),'63.3,64.6']
]
lorem_ipsum = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Aenean mauris libero, efficitur eget tincidunt nec, condimentum ac dui. 
Pellentesque sed velit nisl. 
Morbi congue odio diam, sit amet rutrum tellus porta vitae. 
Mauris ac nisl et ante aliquam sagittis ac quis urna. 
Aenean sed massa lorem. 
Aliquam auctor ultricies enim, eget aliquam nisl. 
Sed magna nisi, laoreet ac consectetur eget, interdum id urna. 
Donec eros metus, dapibus at tempor sit amet, ornare at ante. 
Morbi nec ultrices eros. Aliquam imperdiet tempor libero nec maximus. 
 '''
 
dickbutt = '''
          #####  ### #######   ######  ####### #     # #######    ###
         #     #  #  #         #     # #     # ##    # #          ###
         #        #  #         #     # #     # # #   # #          ###
         #  ####  #  #####     #     # #     # #  #  # #####       #
         #     #  #  #         #     # #     # #   # # #
         #     #  #  #         #     # #     # #    ## #          ###
          #####  ### #         ######  ####### #     # #######    ###

                              MMMMMM=
                         .MMMMMMMMMMMMMM
                       MMMMMM         MMMM
                    MMMMM              MMMMM.
              MMMMMMMM                  ?MMMM.
           .MMMMMMMM7MM                  MMMMM
           MMMMMMMMM MM                   MMMM
           MMMMMMMMM .MM                   MMM
          .MMMMMMM.   MM.M.   =MMMMMMMM.   MMM
           MMMMMMMM.MMMMMM.  MMMMMMMM MMM  MMM
           MMMMMMMMMMMM     MMMMMMMMM  MMM MMM
          MMM    MMM:  MM   MMMMMMMMM  MMM MMM
         8MM.    MMMMMMMM=  MMMMMMMM.  .M ,MM7
        MMMMMMMM..          MMMMM.     M  MMM
       .MMMMMMMMMMMMMMM       MMMMMMMMM.  MMM
      .MMM        MMMMMMMMMMM.           MMMM                    MMMMM
      MMM                .~MMMMMMM.      MMM.                  MMM   MMO
     MMM.                               MMMM                 MMMM     MM
    .MMM                                MMMM                MMM      IMM
    MMM                                DMMM               .MMM.      MM
   MMM                                 MMMM              MMMM       MM.
   MMM                                .MMM              MMM.       MM
  MMM                      MM        .MMM             MMM.       MMM.
 .MMM                     .MM  MM.   MMM~            MMM.      .MMM.'''

