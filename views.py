# encoding: utf-8

import time
import threading
from Tkinter import *
from tieba_new import get_new_video

STOP_SEARCH = True


def search_one():
    global show
    global var

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
    show.insert('1.0', u"搜索中...")
    global STOP_SEARCH
    STOP_SEARCH = False

def set_stop():
    global STOP_SEARCH
    STOP_SEARCH = True


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
    button1.pack(side=LEFT, padx=100)
    button2.pack(side=LEFT)

    search_thd = threading.Thread(target=search)
    search_thd.daemon = True
    search_thd.start()

    # 进入消息循环
    root.mainloop()

# "http://tieba.baidu.com/f?ie=utf-8&kw=%E8%A7%86%E9%A2%91&red_tag=t0121432679"
# "https://tieba.baidu.com/f?kw=javagame&ie=utf-8&tp=0"
