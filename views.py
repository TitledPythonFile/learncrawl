# encoding: utf-8

import time
import threading
from Queue import Queue
from Tkinter import *
from tieba_new import get_new_video, download

STOP_SEARCH = True
url_que = Queue()
once_list = []

def search_one():
    global show
    global input
    global var
    global once_list

    # show.delete(0.0, END)
    url = var.get()
    # print url
    v_list = get_new_video(url)
    if not v_list:
        videos = u"没有最新视频!\n"
    else:
        videos = ''
        for v in v_list:
            videos += v.get("title")
            videos += "\n"
            videos += v.get("url")
            videos += "\n"
            once_list.append(v.get("url"))

    show.insert('1.0', videos)

def search():
    global show
    while True:
        # show.delete(0.0, END)
        if not STOP_SEARCH:
            search_one()
            time.sleep(10)


def set_start():
    # print "start"
    global show
    show.insert('1.0', u"搜索中...\n")
    global STOP_SEARCH
    STOP_SEARCH = False


def set_stop():
    global STOP_SEARCH
    STOP_SEARCH = True


def clear_window():
    show.delete(0.0, END)
    # input.delete(0.0, END)

def download_one():
    while True:
        try:
            url = url_que.get()
        except:
            time.sleep(2)
            continue
        download(url)

def start_download():
    global once_list
    for url in once_list:
        url_que.put(url)
    once_list = []


if __name__ == "__main__":

    root = Tk()
    root.title(u"点击试试")
    root.geometry("400x300")

    lable = Label(root, text="url:")
    lable.pack()

    var = StringVar()
    input = Entry(root, textvariable=var)
    input.pack(pady=10)

    # videos = ""
    # lable1 = Label(root, text=videos)
    # lable1.pack()

    lable = Label(root, text="result:")
    lable.pack()
    show = Text(root, width=50,height=10)
    show.pack()

    button1 = Button(root, text=u"开始", command=set_start)
    button2 = Button(root, text=u"停止", command=set_stop)
    button3 = Button(root, text=u"清空", command=clear_window)
    button4 = Button(root, text=u"下载", command=start_download)
    button1.pack(side=LEFT, padx=40)
    button2.pack(side=LEFT)
    button3.pack(side=LEFT, padx=40)
    button4.pack(side=LEFT)

    search_thd = threading.Thread(target=search)
    search_thd.daemon = True
    search_thd.start()

    download_thd = threading.Thread(target=download_one)
    download_thd.daemon = True
    download_thd.start()

    # 进入消息循环
    root.mainloop()

# "http://tieba.baidu.com/f?ie=utf-8&kw=%E8%A7%86%E9%A2%91&red_tag=t0121432679"
# "https://tieba.baidu.com/f?kw=javagame&ie=utf-8&tp=0"
