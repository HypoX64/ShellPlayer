![image](./imgs/logo_char.png)
# ShellPlayer
| [English](./README.md)  | 中文版 |
你能在终端中看视频，色彩斑斓且富有声音的！！！<br>
你能在终端中看视频，色彩斑斓且富有声音的！！！<br>
你能在终端中看视频，色彩斑斓且富有声音的！！！<br>

## 入门
### 前提要求
* Linux
* python3
* [ffmpeg](http://ffmpeg.org/)
```bash
sudo apt-get install ffmpeg
```
### 依赖
代码依赖于 opencv-python, 可以通过 pip install安装
```bash
pip install opencv-python
```
### 克隆这个仓库
```bash
git clone https://github.com/HypoX64/ShellPlayer.git
cd ShellPlayer
```
### 运行程序
```bash
python play.py -m "视频或者图片的路径"
```
![image](./imgs/kun.gif)<br>
## 更多的参数

|    选项    |        描述         |                 默认值                 |
| :----------: | :------------------------: | :-------------------------------------: |
|  -m | 视频或者图片的路径 |                    './imgs/test.jpg'                    |
| -g | 如果输入则播放黑白的视频 |  |
|    -f    |    播放帧速率, 0-> 自动    |            0 |
| -c | charstyle: 字符输出效果    1 \| 2 \| 3 | 3 |
| -s | 终端尺寸, 1:80X24  2:132X43  3:203X55 |                 1          |
|    --frame_num    |    播放总帧数   0->播放所有的帧    |                 0                  |
| --char_scale | 字符长宽比 | 2.0 |

