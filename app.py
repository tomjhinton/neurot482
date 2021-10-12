from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
img = Image.new('RGBA', (6000, 6000), color='white')
from dotenv import load_dotenv
import tweepy
import os
import io
import sys
import numpy as np
from PIL import Image, ImageFont
import requests
import matplotlib.pylab as plt
import matplotlib.colors as mclr
from random import randint, seed
import json
import math
import PIL

def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

def Random_Alpha():
    l = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    return l[random.randint(0,25)]

def draw_pastell(nx=900, ny=1600, CL=180, rshift=3):
    nz=3
    mid = nx//2
    dCL = 50
    quote_font = ImageFont.truetype('Art-Dystopia-2.ttf', randint(350, 1000))
    quote_font1 = ImageFont.truetype('Passio-Graphis.otf', randint(350, 1000))
    quote_font2 = ImageFont.truetype('FerriteCoreDX-Medium.otf', randint(350, 1000))


    arr = [quote_font, quote_font1, quote_font2]

    #---- show&save grafics ---------
    xa = -1.5
    xb = 1.5
    ya = -2
    yb = 2

    # max iterations allowed
    maxIt = 1000

    # im1 size
    imgx = 800
    imgy = 800
    im2 = Image.new("RGB", (imgx, imgy))
    draw = ImageDraw.Draw(im2)

    offset = 0
    a_frames = []


    c_k = os.getenv("API_key")
    c_s = os.getenv("API_secret_key")
    a_k = os.getenv("Access_token")
    a_s = os.getenv("access_token_secret")
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    api = tweepy.API(auth)


    mapikc= os.getenv('musixmatch')

    albums = ['13467111', '29953335', '21080880']

    trackIds = requests.get(
  'https://api.musixmatch.com/ws/1.1/album.tracks.get?apikey='
  +  mapikc +
  '&album_id=' + albums[randint(0,2)]
)


    ids = trackIds.json()
    print((ids['message']['body']['track_list'][randint(0,len(ids['message']['body']['track_list'])-1 )]["track"]["track_name"]))


    lyrics = requests.get(
      'https://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey='
      + mapikc +
      '&track_id=' + str(ids['message']['body']['track_list'][randint(0,len(ids['message']['body']['track_list'])-1 )]["track"]["track_id"])
    )

    lyrics = lyrics.json()

    i = lyrics['message']['body']['lyrics']['lyrics_body'].upper()
    p = lyrics['message']['body']['lyrics']['lyrics_body'].split('\n')
    p = list(filter(lambda x : len(x) > 4 , p))
    i = i.replace(" ", "")
    for ix in range(len(i)-3):
        draw = ImageDraw.Draw(im2)
        draw.multiline_text((randint(-10, 800),randint(-10, 800)), i[ix], tuple(np.random.randint(256, size=3)), font=arr[randint(0, 2)])
        quote_font = ImageFont.truetype('Art-Dystopia-2.ttf', randint(350, 800))
        quote_font1 = ImageFont.truetype('Passio-Graphis.otf', randint(350, 800))
        quote_font2 = ImageFont.truetype('FerriteCoreDX-Medium.otf', randint(350, 800))
        arr = [quote_font,  quote_font1, quote_font2]
        draw = ImageDraw.Draw(im2)
        im2 = im2.rotate(45)
        im2 = im2.filter(ImageFilter.EDGE_ENHANCE_MORE)
        im2 = im2.filter(ImageFilter.CONTOUR)
        a_frames.append(np.asarray(im2))

    # a_frames = a_frames + a_frames[::-1]
    a = np.stack(a_frames)
    #         quote_font = ImageFont.truetype('Tapeworm-Regular.otf', int(math.ceil(1750/(len(i[ix])+1))) )
    #         draw.multiline_text((30,25+ offset + int(math.ceil(1750/(len(i[ix])+1)))), i[ix], (255, 255, 255), font=quote_font)
    #         offset += 65
    # print(lyrics)

    buf = io.BytesIO()
    ims = [Image.fromarray(a_frame) for a_frame in a]
    ims[0].save(buf, format='GIF', save_all=True, append_images=ims[1:], loop=0, duration=150)
    ims[0].save('out.gif', save_all=True, append_images=ims[1:], loop=0, duration=150)
    buf.seek(0)
    thing = buf.getvalue()
    test = api.media_upload('28.gif',file= buf, chunked = True,
    media_category = "tweet_gif")
    api.update_status(status=p[randint(0,len(p)-3)], media_ids=[test.media_id], )


    print(p[randint(0,len(p)-3)])

draw_pastell(nx=900, ny=1800, CL=181, rshift=3)
