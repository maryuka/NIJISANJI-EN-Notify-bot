# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import logging
import time
import requests
import json

import psycopg2
import tweepy

from tools import twitter_api, db_prepare
tw_api = twitter_api()
from dics import yt_id_dic, tw_id_dic

sl_time = 1


#Returns dict data of YouTube channel subscribers(unsigned long)
#** https://developers.google.com/youtube/v3/docs/channels#resource **
def get_subscriber(names):
    yt_id=[]
    subsc={}

    for name in names:
        yt_id.append(yt_id_dic[name])

    API_KEY = os.environ['YT_API_KEY']
    options = { 'key': API_KEY,
                'id': yt_id,
                'part': 'statistics'}
    time.sleep(sl_time)
    try:
        r = requests.get('https://www.googleapis.com/youtube/v3/channels', params=options, timeout=10)
        data = r.json()
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.exception(f'request failed:{e}')

    for i, name in enumerate(names):
        for member in names:
            if yt_id_dic[member] == data['items'][i]['id']:
                chsubsc = data['items'][i]['statistics']['subscriberCount']
                subsc[member] = int(chsubsc)
                break

    return subsc


#Return the number of Twitter followers(int)
#** https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user **
def get_follower(names):
    tw_id=[]
    follower={}
    i = 0

    for name in names:
        if tw_id_dic[name] != 0:
            tw_id.append(tw_id_dic[name])
        else:
            follower[name] = 0

    try:
        tw_users = tw_api.lookup_users(tw_id)
    except tweepy.TweepError as e:
        logging.exception(f'get followers failed:{e.reason}')

    for i, _ in enumerate(tw_users):
        for member in names:
            if tw_id_dic[member] == tw_users[i].id:
                follower[member] = tw_users[i].followers_count
                break
    return follower

def get_dbdata(yesterday):
    try:
        db = db_prepare()
        result = db.execute_scalor('SELECT log FROM daily_logs WHERE date = \'{:s}\';'.format(yesterday))
        print(result[0])
        return dict(result[0])
    except (Exception, psycopg2.Error) as e:
        logging.exception(f'database error: {e}')
        return None
