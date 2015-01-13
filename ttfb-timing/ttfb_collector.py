#!/usr/bin/env python
"""measure http time to first byte (ttfb) latency for cdn hosted videos"""

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
        urls.append('http://www.xuetangx.com//course-intro?D82C7AACFA056C939C33DC5901307461')
        for url in urls:
            get_ttfb(url)
        time.sleep(TIME_INTERVAL)
