# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import logging
import time
import pickle
import json
import bz2
from codecs import decode

from PIL import Image, ImageDraw, ImageFont
import tweepy
import psycopg2
from psycopg2.extras import Json

from db_ope import PostgreConnect

sl_time = 3
PROTOCOL = pickle.HIGHEST_PROTOCOL


#preparing to tweet and retrieve data via Twitter
def twitter_api():
    CONSUMER_KEY    = os.environ['API_KEY']
    CONSUMER_SECRET = os.environ['API_SECRET_KEY']
    ACCESS_TOKEN    = os.environ['ACCESS_TOKEN']
    ACCESS_SECRET   = os.environ['ACCESS_TOKEN_SECRET']
    auth            = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api             = tweepy.API(auth)

    return api


#generate an image of the previous day's ratio
def img_gen(subscribers_, diff_, members_, today, gen_img_name):
    im = Image.open('img/bg_template.png')
    draw = ImageDraw.Draw(im)
    k = l = 0

    W, H = (2001,3001)

    font_size_num = 60
    font_size_date = 40
    font_num = ImageFont.truetype('font/NixieOne-Regular.ttf', font_size_num)
    font_date = ImageFont.truetype('font/NixieOne-Regular.ttf', font_size_date)
    font_color = (0,0,0)

    w_pos_s = 1200 #distance from the left edge of the image(Location of the center line of Subscribers)
    w_pos_d = 1640 #distance from the left edge of the image(Location of the center line of TheDayBefore)
    h_pos = 290.5 #distance from the top of the image of the value

    w_date, h_date = draw.textsize('{}'.format(today), font=font_date)
    draw.text((W - w_date - 30, H - h_date - 30), '{}'.format(today), font_color, font=font_date)

    for mem in members_:
        for name, subscriber in subscribers_.items():
            if name == mem:
                w_subsc, h_subsc = draw.textsize('{:,}'.format(subscriber), font=font_num)
                
                draw.text((w_pos_s - w_subsc / 2, h_pos + 95.7 * k), '{:,}'.format(subscriber), font_color, font_num)
                k += 1
                break
        for name, diff in diff_.items():
            if name == mem:
                w_diff, h_diff = draw.textsize('+{:,}'.format(diff), font=font_num)
                
                draw.text((w_pos_d - w_diff / 2, h_pos + 95.7 * l), '+{:,}'.format(diff), font_color, font_num)
                l += 1
                break
    im.save(gen_img_name)


#tweet with image
#tweet is the text to tweet, files is the path to the image
def tweet_with_imgs(tweet, file):
    api = twitter_api()
    media_ids = []
    img = api.media_upload(file)
    media_ids.append(img.media_id_string)

    time.sleep(sl_time)
    try:
        api.update_status(status=tweet, media_ids=media_ids)
    except tweepy.TweepError as e:
        logging.exception(f'tweet failed:{e.reason}')
    


def db_prepare():
    USER = os.environ['DB_USER']
    PASSWORD = os.environ['DB_PASS']
    HOST = os.environ['DB_HOST']
    PORT = os.environ['DB_PORT']
    DBNAME = os.environ['DB_DBNAME']

    db = PostgreConnect(HOST,DBNAME,USER,PASSWORD)
    return db
    

def db_create():
    try:
        db = db_prepare()
        if not db.exists('daily_logs'):
            print('create db')
            db.create('daily_logs','date text, log jsonb','date, log')
    except (Exception, psycopg2.Error) as e:
        logging.exception(f'database error: {e}')
        return None


def db_insert(day_num_log, today):
    try:
        db = db_prepare()
        sql = 'INSERT INTO daily_logs (date, log) VALUES (\'{}\', {});'.format(today, Json(day_num_log))
        db.execute(sql)
    except (Exception, psycopg2.Error) as e:
        logging.exception(f'database error: {e}')
        return None


def db_delete(dbname):
    try:
        db = db_prepare()
        db.drop(dbname)
    except (Exception, psycopg2.Error) as e:
        logging.exception(f'database error: {e}')
        return None


# https://www.haya-programming.com/entry/2017/02/25/184006
def ptoz(dict):
    #return dict
    return bz2.compress(pickle.dumps(dict))

def ztop(b):
    #return b
    print(b)
    return pickle.loads(bz2.decompress(b))