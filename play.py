import os
import sys
import time
import multiprocessing
from multiprocessing import Process, Queue
import threading
import subprocess
import numpy as np
import cv2
import platform

from util import util,ffmpeg
from img2shell import Transformer
from options import Options

def readvideo(opt,imgQueue):
    cap = cv2.VideoCapture(opt.media)
    play_index = np.linspace(0, opt.frame_num-1,num=int(opt.frame_num*opt.fps/opt.ori_fps),dtype=np.int64)
    frame_cnt = 0; play_cnt =0
    while(cap.isOpened()):
        _ , frame = cap.read() 
        if frame_cnt == play_index[play_cnt]:
            imgQueue.put(frame)
            if play_cnt < len(play_index)-1:
                play_cnt+= 1
        frame_cnt += 1

def timer(opt,timerQueueime):
    while True:
        t = 1.0/opt.fps
        time.sleep(t)
        timerQueueime.put(True)

opt = Options().getparse()
system_type = 'Linux'
if 'Windows' in platform.platform():
    system_type = 'Windows'

#-------------------------------Media Init-------------------------------
if util.is_img(opt.media):
    img = cv2.imread(opt.media)
    h_media,w_media = img.shape[:2]
elif util.is_video(opt.media): 
    fps,endtime,h_media,w_media = ffmpeg.get_video_infos(opt.media)
    if opt.frame_num == 0:
        opt.frame_num = int(endtime*fps-5)
    if opt.ori_fps == 0:
        opt.ori_fps = fps
    util.makedirs('./tmp')
else:
    print('Can not load this file!')

#-------------------------------Image Shape Init-------------------------------
if opt.screen==1:
    limw = 80;limh = 24
if opt.screen==2:
    limw = 132;limh = 43
if opt.screen==3:
    limw = 203;limh = 55
screen_scale = limh/limw

img_scale = h_media/w_media/opt.char_scale
if img_scale >= screen_scale:
    strshape = (limh,int(limh/img_scale))
else:
    strshape = (int(limw*img_scale),limw)

#-------------------------------img2shell Init-------------------------------
transformer = Transformer(strshape,(limh,limw),opt.charstyle)
if util.is_video(opt.media): 
    recommend_fps = transformer.eval_performance(opt.gray)
    if opt.fps == 0:
        opt.fps = np.clip(recommend_fps,1,opt.ori_fps)
    else:
        opt.fps = np.clip(opt.fps,1,opt.ori_fps)
    if system_type == 'Linux':
        ffmpeg.video2voice(opt.media,'-ar 16000 ./tmp/tmp.wav')

#-------------------------------main-------------------------------
if __name__ == '__main__':
    if system_type == 'Windows':
        multiprocessing.freeze_support()
    if util.is_img(opt.media):
        print(transformer.convert(img,opt.gray))
    elif util.is_video(opt.media):
        imgQueue = Queue(1)
        timerQueue = Queue()

        imgload_p = Process(target=readvideo,args=(opt,imgQueue))
        imgload_p.daemon = True
        imgload_p.start()

        timer_p = Process(target=timer,args=(opt,timerQueue))
        timer_p.daemon = True
        timer_p.start()

        time.sleep(0.5)
        if system_type == 'Linux':
            subprocess.Popen('paplay ./tmp/tmp.wav', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for i in range(int(opt.frame_num*opt.fps/opt.ori_fps)-1):
            timerQueue.get()
            img = imgQueue.get()
            string = transformer.convert(img,opt.gray)
            t=threading.Thread(target=print,args=(string,))
            t.start()
