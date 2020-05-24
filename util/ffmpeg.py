import os,json
import subprocess
# ffmpeg 3.4.6

def run(cmd_str):
    #out_string = os.popen(cmd_str).read()
    #For chinese path in Windows
    #https://blog.csdn.net/weixin_43903378/article/details/91979025
    stream = os.popen(cmd_str)._stream
    out_string = stream.buffer.read().decode(encoding='utf-8')
    return out_string


def video2voice(videopath,voicepath):
    p = subprocess.Popen('ffmpeg -i "'+videopath+'" '+voicepath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sout = p.stdout.readlines()
    # run(cmd_str)

def get_video_infos(videopath):
    cmd_str =  'ffprobe -v quiet -print_format json -show_format -show_streams -i "' + videopath + '"'  
    out_string = run(cmd_str)
    infos = json.loads(out_string)
    try:
        fps = eval(infos['streams'][0]['avg_frame_rate'])
        endtime = float(infos['format']['duration'])
        width = int(infos['streams'][0]['width'])
        height = int(infos['streams'][0]['height'])
    except Exception as e:
        fps = eval(infos['streams'][1]['r_frame_rate'])
        endtime = float(infos['format']['duration'])
        width = int(infos['streams'][1]['width'])
        height = int(infos['streams'][1]['height'])

    return fps,endtime,height,width