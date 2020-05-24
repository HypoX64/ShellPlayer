![image](./imgs/logo_char.png)
# ShellPlayer
| English | [中文版](./README_CN.md) |
You can play colorful & soundful video in shell !!!<br>
You can play colorful & soundful video in shell !!!<br>
You can play colorful & soundful video in shell !!!<br>

## Getting Started
### Prerequisites
* Linux
* python3
* [ffmpeg](http://ffmpeg.org/)
```bash
sudo apt-get install ffmpeg
```
### Dependencies
This code depends on opencv-python, available via pip install.
```bash
pip install opencv-python
```
### Clone this repo
```bash
git clone https://github.com/HypoX64/ShellPlayer.git
cd ShellPlayer
```
### Run program
```bash
python play.py -m "your_video_or_image_path"
```
![image](./imgs/kun.gif)<br>
## More parameters

|    Option    |        Description         |                 Default                 |
| :----------: | :------------------------: | :-------------------------------------: |
|  -m | your video or image path |                    './imgs/test.jpg'                    |
| -g | if specified, play gray video |  |
|    -f    |    playing fps, 0-> auto    |            0 |
| -c | charstyle: style of output    1 \| 2 \| 3 | 3 |
| -s | size of shell, 1:80X24  2:132X43  3:203X55 |                 1          |
|    --frame_num    |    how many frames want to play   0->all    |                 0                  |
| --char_scale | character aspect ratio in shell | 2.0 |

