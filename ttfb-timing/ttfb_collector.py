#!/usr/bin/env python
"""measure http time to first byte (ttfb) latency for cdn hosted videos"""

import json
import time
from timeit import default_timer
import urllib2


TIME_INTERVAL = 10  # secs
RESULTS = 'results.log'
ERROR = 'errors.log'


def log_error(human_time, epoch, url, error_msg):
    msg = '{}, {}, {}, {}'.format(human_time, epoch, url, error_msg)
    with open(ERROR, 'a') as f:
        f.write('{}\n'.format(msg))
    print(msg)


def log_success(human_time, epoch, url, ttfb):
    msg = '{}, {}, {}, {}'.format(human_time, epoch, url, ttfb)
    with open(RESULTS, 'a') as f:
        f.write('{}\n'.format(msg))
    print(msg)


def get_xuetang_api_url(url):
    human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    epoch = time.time()
    try:
        resp = urllib2.urlopen(url)
        data = resp.read()
        resp.close()
    except urllib2.HTTPError as e:
        log_error(human_time, epoch, url, e.code)
    except urllib2.URLError as e:
        log_error(human_time, epoch, url, e.reason)
    json_data = json.loads(data)
    return json_data[u'sources'][0]


def get_ttfb(url):
    human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    epoch = time.time()
    start_time = default_timer()
    try:
        resp = urllib2.urlopen(url)
        resp.read(1)
        resp.close()
    except urllib2.HTTPError as e:
        log_error(human_time, epoch, url, e.code)
    except urllib2.URLError as e:
        log_error(human_time, epoch, url, e.reason)
    else:
        end_time = default_timer()
        ttfb = (end_time - start_time) * 1000
        log_success(human_time, epoch, url, ttfb)


if __name__ == '__main__':
    while True:
        urls = []
        urls.append('http://video.study.163.com/edu-video/nos/mp4/2014/06/23/460097_hd.mp4')
        urls.append('http://d2f1egay8yehza.cloudfront.net/TSGCMATH/TSGCMATHT314-V000400_DTH.mp4')
        lookup_url = 'http://api.xuetangx.com/edx/video?s3_url=https://s3.amazonaws.com/edx-course-videos/mit-600x/M-600X-FA12-L3-Intro_100.mp4'
        urls.append(get_xuetang_api_url(lookup_url))
        for url in urls:
            get_ttfb(url)
        time.sleep(TIME_INTERVAL)
