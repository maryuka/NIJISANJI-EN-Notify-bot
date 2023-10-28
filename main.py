# -*- coding: utf-8 -*-
from __future__ import print_function
import time
from datetime import datetime, timezone, timedelta
import pickle
import os

import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

from tools import twitter_api, img_gen, tweet_with_imgs, db_create, db_insert, db_delete, ptoz, ztop
api = twitter_api()
from get_data import get_subscriber, get_follower, get_dbdata
from dics import members, yt_url_dic, tw_id_dic

sl_time = 1
rn_time = 1   #how often do you get the number of subscribers and followers every few minutes?

num_log_file = './num_log_file_{}.pickle'
diff_img = './diff.png'

#Japan Standard Time
JST = timezone(timedelta(hours=9), name='JST')
#Eastern Daylight Time
#(2:00AM 2nd Sunday in March to 2:00AM 1st Sunday in November)
EDT = timezone(timedelta(hours=-4), name='EDT')
#Eastern Standard Time
EST = timezone(timedelta(hours=-5), name='EST')

member_all = [members]


#get a number and tweet it if the condition is met.
def number_notification(members_, num):
    print('number_notification start')
    start_ = time.time()
    num_log_file_ = num_log_file.format(num)
    tweet_head = ''
    contents = {}

    #get data from Twitter and YouTube
    subscribers = get_subscriber(members_)
    followers = get_follower(members_)
    for member in members_:
        follower = followers[member]
        subscriber = subscribers[member]
        contents_in = { 'follower': follower, 'subscriber': subscriber}
        contents.update({member : contents_in})

    #get the previous data
    if not os.path.exists(num_log_file_):
        with open(num_log_file_, 'wb') as pi:
            pickle.dump(contents, pi)
    with open(num_log_file_, 'rb') as pi:
        old_contents = pickle.load(pi)

    #set the conditions for tweeting in increments of th_val people.
    #th_val = 10000 then 10000 people.
    def _judge(member, key, th_val=1000):
        if key in contents[member].keys():
            if contents[member][key] // th_val > old_contents[member][key] // th_val:
                return True
            else:
                return False
        else:
            return False

    #if the bot tries to tweet the same tweet as the last 50 tweets, cancel it.
    try:
        recent_tweets = api.user_timeline(count=50)
    except tweepy.TweepError as e:
        print(f'tweet_failure:{e.reason}')
    recent_tweets = [tweet.text for tweet in recent_tweets]
    def _tw_cancel(tweet):
        flags = [r_tweet.split('(')[0] in tweet for r_tweet in recent_tweets]
        if sum(flags) == 0:
            return True
        else:
            print('CANCELLED : ', tweet)
            return False

    #post tweet
    def _post_tweet(type,tweet,url):
        if type == 'TW':
            tweet += '(Twitter : twitter.com/{})\n'.format(url)
        elif type == 'YT':
            tweet += '(YouTube : {})\n'.format(url)
        if _tw_cancel(tweet):
            time.sleep(sl_time)
            try:
                api.update_status(tweet)
            except tweepy.TweepError as e:
                print(f'tweet_failure:{e.reason}')
            print('number_notification')
            print('Tweeted.')

    #Every 10,000 subscribers reached will add general hashtag
    for member in members_:
        if _judge(member, 'follower'):
            str_follower = str(contents[member]['follower']//1000)
            try:
                tw_url = api.get_user(tw_id_dic[member]).screen_name
            except tweepy.TweepError as e:
                print(f'tweet_failure:{e.reason}')
            tweet_head = '[Twitter followers notification]\n\n'
            if str_follower[-1] == '0' and not member == 'NIJISANJI EN Official':
                tweet = '#{} has reached {:,} followers on Twitter.\n' \
                         .format(member.replace(' ', ''), int(str_follower+'000'))
            else:
                tweet = '{} has reached {:,} followers on Twitter.\n' \
                         .format(member, int(str_follower+'000'))
            _post_tweet('TW',tweet,tw_url)
        if _judge(member, 'subscriber'):
            str_subscriber = str(contents[member]['subscriber']//1000)
            tweet_head = '[YouTube subscribers notification]\n\n'
            if str_subscriber[-1] == '0' and not member == 'NIJISANJI EN Official':
                tweet = '#{} has reached {:,} subscribers on YouTube.\n' \
                         .format(member.replace(' ', ''), int(str_subscriber+'000'))
            else:
                tweet = '{} has reached {:,} subscribers on YouTube.\n' \
                         .format(member, int(str_subscriber+'000'))
            _post_tweet('YT',tweet,yt_url_dic[member])
        
        #Notification every 5,000 subscribers, and every 1,000 subscribers before 5,000 of 100,000.
        ''' 
        if _judge(member, 'follower'):
            tw_url = api.get_user(tw_id_dic[member]).screen_name
            str_follower = str(contents[member]['follower']//1000)
            tweet_head = '[Twitter followers notice]\n\n'
            if str_follower[-2] == '9':
                if str_follower[-1] == '5':
                    tweet  = tweet_head + '{} has reached {:,} followers on Twitter.\n5000 followers left to {}K.\n' \
                        .format(member_, int(str_follower+'000'), (contents[member]['follower']//10000+1)*10)
                    _post_tweet('TW',tweet,tw_url)
                elif str_follower[-1] == '6':
                    tweet  = tweet_head + '{} has reached {:,} followers on Twitter.\n4000 followers left to {}K.\n' \
                        .format(member_, int(str_follower+'000'), (contents[member]['follower']//10000+1)*10)
                    _post_tweet('TW',tweet,tw_url)
                elif str_follower[-1] == '7':
                    tweet  = tweet_head + '{} has reached {:,} followers on Twitter.\n3000 followers left to {}K.\n' \
                        .format(member_, int(str_follower+'000'), (contents[member]['follower']//10000+1)*10)
                    _post_tweet('TW',tweet,tw_url)
                elif str_follower[-1] == '8':
                    tweet  = tweet_head + '{} has reached {:,} followers on Twitter.\n2000 followers left to {}K.\n' \
                        .format(member_, int(str_follower+'000'), (contents[member]['follower']//10000+1)*10)
                    _post_tweet('TW',tweet,tw_url)
                elif str_follower[-1] == '9':
                    tweet  = tweet_head + '{} has reached {:,} followers on Twitter.\n1000 followers left to {}K.\n' \
                        .format(member_, int(str_follower+'000'), (contents[member]['follower']//10000+1)*10)
                    _post_tweet('TW',tweet,tw_url)
            elif str_follower[-1] == '0':
                tweet = '#{} has reached {:,} followers on Twitter.\n' \
                                        .format(member_.replace(' ', ''), int(str_follower+'000'))
                _post_tweet('TW',tweet,tw_url)
            elif str_follower[-1] == '5':
                tweet = '{} has reached {:,} followers on Twitter.\n' \
                                        .format(member_, int(str_follower+'000'))
                _post_tweet('TW',tweet,tw_url)

        if _judge(member, 'subscriber'):
            str_subscriber = str(contents[member]['subscriber']//1000)
            tweet_head = '[YouTube subscribers notice]\n\n'
            if str_subscriber[-2] == '9':
                if str_subscriber[-1] == '5':
                    tweet  = tweet_head + '{} has reached {:,} subscribers on YouTube.\n5000 subscribers left to {}K.\n' \
                        .format(member_, int(str_subscriber+'000'), (contents[member]['subscriber']//10000+1)*10)
                    _post_tweet('YT',tweet,yt_url_dic)
                elif str_subscriber[-1] == '6':
                    tweet  = tweet_head + '{} has reached {:,} subscribers on YouTube.\n4000 subscribers left to {}K.\n' \
                        .format(member_, int(str_subscriber+'000'), (contents[member]['subscriber']//10000+1)*10)
                    _post_tweet('YT',tweet,yt_url_dic)
                elif str_subscriber[-1] == '7':
                    tweet  = tweet_head + '{} has reached {:,} subscribers on YouTube.\n3000 subscribers left to {}K.\n' \
                        .format(member_, int(str_subscriber+'000'), (contents[member]['subscriber']//10000+1)*10)
                    _post_tweet('YT',tweet,yt_url_dic)
                elif str_subscriber[-1] == '8':
                    tweet  = tweet_head + '{} has reached {:,} subscribers on YouTube.\n2000 subscribers left to {}K.\n' \
                        .format(member_, int(str_subscriber+'000'), (contents[member]['subscriber']//10000+1)*10)
                    _post_tweet('YT',tweet,yt_url_dic)
                elif str_subscriber[-1] == '9':
                    tweet  = tweet_head + '{} has reached {:,} subscribers on YouTube.\n1000 subscribers left to {}K.\n' \
                        .format(member_, int(str_subscriber+'000'), (contents[member]['subscriber']//10000+1)*10)
                    _post_tweet('YT',tweet,yt_url_dic)
            if str_subscriber[-1] == '0':
                tweet = '#{} has reached {:,} subscribers on YouTube.\n' \
                                        .format(member_.replace(' ', ''), int(str_subscriber+'000'))
                _post_tweet('YT',tweet,yt_url_dic)
            if str_subscriber[-1] == '5':
                tweet = '{} has reached {:,} subscribers on YouTube.\n' \
                                    .format(member_, int(str_subscriber+'000'))
                _post_tweet('YT',tweet,yt_url_dic)
        '''
    with open(num_log_file_, 'wb') as pi:
        pickle.dump(contents, pi)

    measure_time = time.time() - start_
    if measure_time > 60 * rn_time:
        print('Too hard work on number_notification')


#Post an embedded image with the current number of registrations and the increase compared to 24 hours ago
def a_day_log_img(members_):
    diff={}
    db_create()
    today = datetime.today()

    now_jst = datetime.now(JST).strftime('%Y/%m/%d %I:%M%p(%Z)')
    now_utc = datetime.now(timezone.utc).strftime('%Y/%m/%d %I:%M%p(%Z)')
    now_edt = datetime.now(EDT).strftime('%Y/%m/%d %I:%M%p(%Z)')

    subscribers = get_subscriber(members_)

    yesterday = today - timedelta(days=1)
    day_num_log_file = get_dbdata(datetime.strftime(yesterday, '%Y-%m-%d'))
    if day_num_log_file == None:
        day_num_log_file = subscribers
    day_before_contents = day_num_log_file

    for mem in members_:
        diff[mem] = subscribers[mem] - day_before_contents[mem]

    img_gen(subscribers, diff, members_, datetime.strftime(today, '%Y-%m-%d'), diff_img)

    tweet = '[subscriber count routine notification]\n'
    tweet += '{}\n{}\n{}'.format(now_edt, now_utc, now_jst)

    tweet_with_imgs(tweet, diff_img)
    print('Image tweeted')

    day_num_log_file = subscribers
    db_insert(day_num_log_file, today.strftime('%Y-%m-%d'))



# main
if __name__ == '__main__':
    start_ = time.time()
    print('Start work : {}'.format(datetime.now()))

    for ii, mem_ in enumerate(member_all):
        print('test number_not : {} : {}'.format(ii, mem_))
        number_notification(mem_, ii+1)
        sched.add_job(number_notification, 'interval', minutes=rn_time, args=[mem_, ii+1])

    #Posting of images of daily increase at 0:00 UTC each day
    #db_delete('daily_logs')
    #a_day_log_img(members)
    #sched.add_job(a_day_log_img, 'interval', hours=1, args=[members])
    sched.add_job(a_day_log_img, 'cron', hour=9, args=[members])

    print(time.time() - start_)

    print('sched work start')
    sched.start()