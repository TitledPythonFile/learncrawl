# encoding: utf-8
"""
采集逻辑:
5分钟检测一次,
5分钟之内的视频链接会被打印
同时视频会被下载,保存名称是时间戳
保存路径是当前文件夹

依赖包:
pyquery--网页分析工具
pip install pyquery

启动方式:
python tieba_new.py url
url 是参数,应为贴吧链接
"""
import re
import sys
import time
import json
import requests
from pyquery import PyQuery as pq

all = set()

# 下载视频的函数
def download(url):
    # url = "http://tb-video.bdstatic.com/tieba-smallvideo-transcode/39947531_6faf7550cae64e14d06a2e963e9404e3_7fd6f25a_2.mp4?authorization=bce-auth-v1%2Fde94045c2e42438fad71ab8df47a6727%2F2017-08-04T08%3A03%3A35Z%2F1800%2F%2F85fd245bec17924f375572493aa8c11ed6856f8d05181eefe05009a6e77b4b51"

    try:
        session = requests.Session()
        r = session.get(url)
    except:
        return
    name = str(int(time.time()))
    path = name + ".mp4"
    with open(path,"wb") as f:
        f.write(r.content)


# 获取近5分钟的视频链接
def get_url(web_url):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'zh-CN,zh;q=0.8',
        'Host': 'tieba.baidu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    session = requests.Session()
    try:
        r = session.get(web_url,headers=headers,timeout=2)  # 请求网页
    except:
        return False,[]

    text = r.text

    # with open('shouye.html','r') as f:
    #     text = f.read()

    comment = re.findall('<ul id="thread_list"(.*)</ul>',text,re.S)

    if not comment:
        return False,[]

    html  = pq(comment[0])  # 分析网页

    tiezi = html('li.j_thread_list')

    last_video = []
    for t in tiezi.items():
        tiezi_url =  t('a.j_th_tit').attr('href')
        title = t('a.j_th_tit').attr('title')
        video_url = t('div.threadlist_video').find('a').attr('data-video')
        one = {
            "title":title,
            "url":video_url,
        }

        # print title, tiezi_url, video_url
        if video_url:
            detail_url = "http://tieba.baidu.com" + tiezi_url
            pub_time = get_time(detail_url)
            time_tup = time.strptime(pub_time, "%Y-%m-%d %H:%M")
            time_str = int(time.mktime(time_tup))
            # now = time.localtime(time.time())
            now = int(time.time())
            # if now.tm_hour == time_tup.tm_hour and (now.tm_min - time_tup.tm_min <= 5):
            if now - time_str <= 300:
                if video_url not in all:
                    all.add(video_url)
                    last_video.append(one)


    # print all
    return True, last_video

# 通过url获取到帖子发布时间
def get_time(url):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'zh-CN,zh;q=0.8',
        'Host': 'tieba.baidu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    session = requests.Session()
    try:
        r = session.get(url,headers=headers)
    except:
        return ""

    html = pq(r.content)

    father_div = html('#j_p_postlist').children("div.l_post.j_l_post.l_post_bright.noborder")
    data_field = father_div.attr("data-field")

    try:
        data = json.loads(data_field)
        date = data["content"]["date"]
    except:
        return ""

    # print date
    return date

# 实时检测,写了一个死循环
def crawl(url):
    while True:

        err_count = 0
        ret, videos = get_url(url)

        while not ret and err_count < 3:
            err_count += 1
            ret, videos = get_url(url)

        if ret:
            if not videos:
                print u"没有最新视频!"
            else:
                for v in videos:
                    print v
                    download(v)
                print u"下载完成!"

        # 定时300秒
        time.sleep(10)

def get_new_video(url):
    err_count = 0
    videos = []
    try:
        ret, videos = get_url(url)
    except:
        ret = False
    while not ret and err_count < 3:
        err_count += 1
        try:
            ret, videos = get_url(url)
        except:
            continue
    return videos


if __name__ == "__main__":
    web_url = sys.argv[1]
    # web_url = 'http://tieba.baidu.com/f?ie=utf-8&kw=%E8%A7%86%E9%A2%91&red_tag=t0121432679'
    # get_url(web_url)
    crawl(web_url)

    # detail_url = "http://tieba.baidu.com/p/5252992647?fid=1252235"
    # get_time(detail_url)