import argparse

class Options():
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.initialized = False

    def initialize(self):
        self.parser.add_argument('-m','--media', type=str, default='./imgs/test.jpg',help='your video or image path')
        self.parser.add_argument('-g','--gray', action='store_true', help='if specified, play gray video')
        self.parser.add_argument('-f','--fps', type=int, default=0,help='playing fps, 0-> auto')
        self.parser.add_argument('-c','--charstyle', type=int, default=1,help='style of output')
        self.parser.add_argument('-s','--screen', type=int, default=1,help='size of shell   1:80*24  2:132*43  3:203*55')

        self.parser.add_argument('--ori_fps', type=int, default=0,help='original fps for video, 0-> auto')
        self.parser.add_argument('--frame_num', type=int, default=0,help='how many frames want to play   0->all')
        self.parser.add_argument('--char_scale', type=float, default=2.0,help='')
        

        self.initialized = True

    def getparse(self):
        if not self.initialized:
            self.initialize()
        self.opt = self.parser.parse_args()
        return self.opt

