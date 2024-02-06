from dics import members, groups
from get_data import get_subscriber
from tools import img_gen, post_tweet_with_imgs, post_tweet, make_ranking
from db_ope import MySQLConnect

import locale
import pickle
import os

from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.blocking import BlockingScheduler

# the interval of getting the number of subscribers(minuts)
INTERVAL_TIME   = 5

NUM_LOG_FILE    = './num_log_file.pickle'
DIFF_IMG_PATHS  = ['./diff1.png','./diff2.png']
DIFF_IMG_PATHS_MONTH  = ['./diff1_month.png','./diff2_month.png']

REMAIN_NOTIFY   = '{hashtag}{member} has more 1,000 subs to go to reach {goal_count:,d} subs on YouTube. ({sub_count:,d} subs)'
SUB_NOTIFY      = '{hashtag}{member} has reached {sub_count:,d} subs on YouTube. ({sub_count:,d} subs)'
DAILY_IMG       = '[Routine Notices] {now_utc_str}\nday-before comparison'
DAILY_RANKING   = '[Daily Ranking] {now_utc_str}\nTop 5 with the highest increase\n'
MONTHLY_IMG     = '[Monthly Notices] {now_utc_str}\n{last_month} period\nmonth-before comparison'
MONTHLY_RANKING = '[Monthly Ranking] {now_utc_str}\nTop 10 with the highest increase\n'

MEMBERS         = members
GROUPS          = groups

locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
SQL = MySQLConnect()

def main():
    print('Start work : {}'.format(datetime.now()))

    SQL.db_create()
    sched = BlockingScheduler()

    # test run
    number_notification()
    daily()

    # Execute number_notification every interval_time minutes
    sched.add_job(number_notification, 'interval',
                  minutes=INTERVAL_TIME)
    # Post a image of daily increase at 0:00 UTC each day
    sched.add_job(daily, 'cron', hour=0,
                  minute=0, second=0)
    # Post a image of monthly increase at the first of each month
    sched.add_job(monthly, 'cron', day=1, hour=0,
                  minute=0, second=0)
    print('sched work start')
    sched.start()

def number_notification():
    '''
    get YouTube subscriber counts and tweet it if the condition is met.

    Parameters
    ----------
    _members : dict
        the dictionary of monitored names in dics.py
    '''
    print('number_notification run')
    
    # --- get current subs and previous subs ---
    def _setup():
        subs = get_subscriber(MEMBERS)

        contents = {}
        for member in MEMBERS:
            mem_subs_num    = subs[member]
            contents_in     = {'subscriber': mem_subs_num}
            contents.update({member: contents_in})

        if not os.path.exists(NUM_LOG_FILE):
            with open(NUM_LOG_FILE, 'wb') as pi:
                pickle.dump(contents, pi)
        with open(NUM_LOG_FILE, 'rb') as pi:
            old_contents = pickle.load(pi)
        return contents, old_contents

    # --- judge if the subs changed ---
    def _judge(member):
        if (contents[member]['subscriber']//1000) > (old_contents[member]['subscriber']//1000):
            return True
        else:
            return False

    # --- post the subscriber count notice ---
    # SUB_NOTIFY    : usually tweet with this
    # REMAIN_NOTIFY : tweet with this when the remaining
    #                 to go to hit every 10,000 subscribers is 1,000
    def _post(member):
        if member in GROUPS:
            h = ''
            member = member
        else:
            h = '#'
            member = member.replace(' ','').replace('.','')
        if sub_count_str[-4]=='9':
            tweet = REMAIN_NOTIFY.format(hashtag=h,member = member,
                                            sub_count=sub_count,goal_count=sub_count+1000)
            post_tweet(tweet)
        else:
            tweet = SUB_NOTIFY.format(hashtag=h,member=member, sub_count=sub_count)
            post_tweet(tweet)

    contents, old_contents = _setup()

    # tweet with a general hashtag every 1,000 subscribers
    for member in MEMBERS:
        sub_count       = contents[member]['subscriber']
        sub_count_str   = str(sub_count)
        if _judge(member):
            _post(member)
    
    # save this data
    with open(NUM_LOG_FILE, 'wb') as pi:
        pickle.dump(contents, pi)

def daily():
    '''
    Post an image with the current subs
    and the increase compared to 24 hours ago

    Post daily top 5 of the increase

    Parameters
    ----------
    _members : dict
        the dictionary of monitored names in dics.py

    Notes
    ----------
    the template image is here :
        img/bg_template1.png, img/bg_template2.png
    '''
    now_utc     = datetime.now(timezone.utc)
    now_utc_str = now_utc.strftime('%Y/%m/%d')

    # --- get current subs and yesterday's data 
    #     and culculate the differences ---
    def _setup():
        subs = get_subscriber(MEMBERS)

        yesterday           = now_utc - timedelta(days=1)
        day_before_contents = SQL.db_get_log(datetime.strftime(yesterday, '%Y-%m-%d'))
        if day_before_contents == None:
            day_before_contents = subs

        diffs = {}
        for mem in MEMBERS:
            diffs[mem] = subs[mem] - day_before_contents[mem]
        return subs, diffs

    # --- post the daily ranking ---
    def _post_ranking():
        tweet       = DAILY_RANKING.format(now_utc_str=now_utc_str)
        tweet_list  = make_ranking(5, MEMBERS, subs, diffs)
        for tw in tweet_list:
            tweet  += ''.join(tw)
            post_tweet(tweet)
            print(tweet)
            tweet   = ''
        print('Ranking tweeted')

    subs, diffs = _setup()

    # save today's data into database
    # SQL.db_insert(subs, now_utc.strftime('%Y-%m-%d'))

    # tweet the img with these diff
    img_gen(subs, diffs, MEMBERS, datetime.strftime(now_utc, '%Y-%m-%d'), DIFF_IMG_PATHS )
    tweet = DAILY_IMG.format(now_utc_str=now_utc_str)
    post_tweet_with_imgs(tweet, DIFF_IMG_PATHS)
    print('Image tweeted')

    _post_ranking()

def monthly():
    '''
    Post an image with the current number of registrations
    and the increase compared to a month ago

    Post monthly top 5 of the increase

    Parameters
    ----------
    _members : dict
        the dictionary of monitored names in dics.py

    Notes
    ----------
    the template image is here :
        img/bg_month_template1.png, img/bg_month_template2.png
    '''
    now_utc     = datetime.now(timezone.utc)
    now_utc_str = now_utc.strftime('%Y/%m/%d')
    last_month  = now_utc - relativedelta(months=1)

    # --- get current subs and last month's data 
    #     and culculate the differences ---
    def _setup():
        subs = get_subscriber(MEMBERS)
        
        month_before_contents = SQL.db_get_log(datetime.strftime(last_month, '%Y-%m-%d'))
        if month_before_contents == None:
            month_before_contents = subs

        diff = {}
        for mem in MEMBERS:
            diff[mem] = subs[mem] - month_before_contents[mem]

        return subs, diff

    # --- post the monthly ranking ---
    def _post_ranking():
        tweet       = MONTHLY_RANKING.format(now_utc_str=now_utc_str)
        tweet_list  = make_ranking(10, MEMBERS, subs, diff)
        thread_id   = None
        for tw in tweet_list:
            tweet       += ''.join(tw)
            thread_id   = post_tweet(tweet,thread_id)
            tweet       = ''
        print('Ranking tweeted')

    subs, diff = _setup()

    # tweet the img with these diff
    img_gen(subs, diff, MEMBERS, datetime.strftime(last_month, '%Y-%m'), DIFF_IMG_PATHS_MONTH)
    tweet = MONTHLY_IMG.format(now_utc_str=now_utc_str,last_month=datetime.strftime(last_month, '%B'))
    post_tweet_with_imgs(tweet, DIFF_IMG_PATHS_MONTH)

    _post_ranking()

    # delete all data
    SQL.db_delete_table()
    # save today's data into database
    SQL.db_create()
    SQL.db_insert(subs, now_utc.strftime('%Y-%m-%d'))


# main
if __name__ == '__main__':
    main()