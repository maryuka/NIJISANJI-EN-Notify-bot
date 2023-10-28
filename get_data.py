# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import logging
import time
import requests
from dics import yt_id_dic

sl_time = 2


def get_subscriber(members):
    '''
    Returns dict data of YouTube channel subscribers

    Parameters
    ----------
    members : list : the list of monitored names in dics.py

    Returns
    ----------
    subs_dict : dict : the dict of pairs of liver names and subs counts
        example {name:subscriber count, ...}

    Notes
    ----------
    YouTube v3 API
    https://developers.google.com/youtube/v3/docs/channels#resource

    '''
    yt_id=[]
    subs_dict={}

    for name in members:
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

    for i, name in enumerate(members):
        for member in members:
            if yt_id_dic[member] == data['items'][i]['id']:
                subs = data['items'][i]['statistics']['subscriberCount']
                subs_dict[member] = int(subs)
                break

    return subs_dict
