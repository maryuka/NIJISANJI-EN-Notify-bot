# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import logging
import time
from PIL import Image, ImageDraw, ImageFont
import tweepy
import pandas as pd

sl_time = 10

# preparing to tweet and retrieve data via Twitter
def twitter_api():
    ACCESS_TOKEN        = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    API_KEY             = os.environ['API_KEY']
    API_SECRET_KEY      = os.environ['API_SECRET_KEY']

    Client = tweepy.Client(
        consumer_key        = API_KEY,
        consumer_secret     = API_SECRET_KEY,
        access_token        = ACCESS_TOKEN,
        access_token_secret = ACCESS_TOKEN_SECRET
    )

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return Client, api

def post_tweet(tweet, thread_id=None):
    '''
    post tweet and return the tweet id

    Parameters
    ----------
    tweet       : str : tweet text
    thread_id   : str : this new tweet reply to this thread_id

    Returns
    ----------
    parent_tweet.data['id'] : str : the tweet id
    '''
    Client, api = twitter_api()
    time.sleep(sl_time)
    try:
        parent_tweet = Client.create_tweet(text = tweet, in_reply_to_tweet_id=thread_id)
        print('Tweeted.')
        return parent_tweet.data['id']
    except tweepy.errors.TweepyException as e:
        print(f'tweet failed:{e}')

def post_tweet_with_imgs(tweet, files):
    '''
    post tweet with images and return the tweet id

    Parameters
    ----------
    tweet       : str : tweet text
    files       : list :  paths to the image files (path is str)

    Returns
    ----------
    parent_tweet.data['id'] : str : the tweet id
    '''
    Client, api = twitter_api()
    media_ids   = []

    try:
        for file in files:
            img = api.media_upload(file)
            media_ids.append(img.media_id)
        time.sleep(sl_time)
    except tweepy.errors.TweepyException as e:
        logging.exception(f'media upload failed:{e}')

    try:
        parent_tweet = Client.create_tweet(text = tweet, media_ids=media_ids)
        time.sleep(sl_time)
        print('Image tweeted')
        return parent_tweet.data['id']
    except tweepy.errors.TweepyException as e:
        logging.exception(f'tweet with media failed:{e}')


def img_gen(subscribers, diffs, members, date, gen_img_paths):
    '''
    make daily or monthly image and save image in gen_img_paths

    Parameters
    ----------
    subscribers     : dict : pairs of liver names and subs count
    diffs           : dict : pairs of liver names and the increase
    members         : list : the list of monitored names in dics.py
    date            : dict : pairs of liver names and subs count
    gen_img_paths   : list : paths to the image files (path is str)
    month           : boolean : if this image is monthly one

    Returns
    ----------
    None
    '''

    im1 = Image.open('img/bg_template1.jpg')
    im2 = Image.open('img/bg_template2.jpg')
    im  = [im1,im2]

    # initialize
    k = l = 0
    W, H            = (2001, 2801)
    font_size_num   = 60
    font_size_date  = 40
    font_num        = ImageFont.truetype('font/NixieOne-Regular.ttf', font_size_num)
    font_date       = ImageFont.truetype('font/NixieOne-Regular.ttf', font_size_date)
    font_color      = (0, 0, 0)
    
    draw            = ImageDraw.Draw(im1)
    w_date, h_date  = draw.textsize('{}'.format(date), font=font_date)
    for _im in im:
        ImageDraw.Draw(_im).text((W - w_date - 30, H - h_date - 30),
            '{}'.format(date), font_color, font=font_date)

    # distance from the left edge of the image(Location of the center line of Subscribers)
    w_pos_s = 1200
    # distance from the left edge of the image(Location of the center line of TheDayBefore)
    w_pos_d = 1640
    # distance from the top of the image of the value
    h_pos   = 380
    # the date position
    w_date, h_date = draw.textsize('{}'.format(date), font=font_date)

    for mem in members:
        if mem == 'Doppio Dropscythe':
            k = l = 0
            draw = ImageDraw.Draw(im2)
        for name, subscriber in subscribers.items():
            if name == mem:
                w_subsc, h_subsc = draw.textsize(
                    f'{subscriber:,}', font=font_num)
                draw.text((w_pos_s - w_subsc / 2, h_pos + 95.7 * k),
                          f'{subscriber:,}', font_color, font_num)
                k += 1
                break

        for name, diff in diffs.items():
            if name == mem:
                if diff>=0:
                    w_diff, h_diff = draw.textsize(
                        f'+{diff:,}', font=font_num)
                elif diff<0:
                    w_diff, h_diff = draw.textsize(
                        f'{diff:,}', font=font_num)
                draw.text((w_pos_d - w_diff / 2, h_pos + 95.7 * l),
                        f'{diff:,}', font_color, font_num)
                l += 1
                break
    i = 0
    for _im in im:
        _im.save(gen_img_paths[i])
        i += 1

def make_ranking(num,members,subs,diff):
    '''
    make ranking of the increase subscriber

    Parameters
    ----------
    num     : int : how many persons do you tweet from the top
    members : list : the list of monitored names in dics.py
    subs    : dict : pairs of liver names and subs count
    diff    : dict : pairs of liver names and the increase

    Returns
    ----------
    tweet_list  : list of tweet text (tweet is separated every 5 person)
    '''
    list    = []

    for member in members:
        l = [member, diff[member]]
        list.append(l)

    df = pd.DataFrame(list,columns=['member','diff'])

    df_top          = df.nlargest(num,'diff')
    df_top['rank']  = df_top['diff'].rank(ascending=False,method='min')
    df_top          = df_top.sort_values('rank')
    rank_list       = df_top.reset_index().values.tolist()

    flag = 0
    tweet = ''
    tweet_list=[]
    for item in rank_list:
        _mem    = item[1]
        _diff   = item[2]
        if(_diff<=0):
            break
        _rank   = int(item[3])
        _sub    = subs[_mem]
        tweet += f'{_rank:d}. {_mem} {_sub:,d} subs (+{_diff:,d})'
        if(flag==4):
            tweet_list.append(tweet)
            tweet = ''
            flag = 0
        else:
            tweet += '\n'
            flag += 1
    return tweet_list
