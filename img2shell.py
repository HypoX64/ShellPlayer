import numpy as np
import cv2
import time

'''
#norm
red       31m   204,0,0
green     32m   78,145,6
brown     33m   196,160,0
blue      34m   52,101,164
cyan-blue 36m   6,152,154

#highlight
#gray     30m   85, 87, 83
red       31m   239,41 ,41
green     32m   138,226,52
yellow    33m   253,233,79
blue      34m   114,159,207 
purple    35m   173,127,168
blue_sky  36m   52 ,226,226
white     37m   238,238,238
'''
def char_add_color(char,color_num):
    if color_num > 4:
        return '\033[1;3'+str(color_num+1-5)+'m'+char+'\033[0m'
    elif color_num == 4:
        return '\033[36m'+char+'\033[0m'
    elif color_num == 3:
        return '\033[34m'+char+'\033[0m'
    elif color_num == 2:
        return '\033[33m'+char+'\033[0m'
    elif color_num == 1:
        return '\033[32m'+char+'\033[0m'
    elif color_num == 0:
        return '\033[31m'+char+'\033[0m'


class Transformer(object):
    def __init__(self, strshape,scshape,charstyle=3):
        super(Transformer, self).__init__()
        self.strshape = strshape
        self.scshape = scshape
        self.strh,self.strw = self.strshape[:2]
        self.sch,self.scw = self.scshape[:2]
        self.ord = 2
        if charstyle == 1:
            self.chars=[' ', ',', '+', '1', 'n','D','&','M','@']
        elif charstyle == 2:
            self.chars=[' ', '▏', '▎', '▍', '▌','▋','▊','▉','█']
        elif charstyle == 3:
            self.chars=[' ', '▏', '▂', '▍', '▅','▋','▇','▉','█']

        self.char_length = len(self.chars)
        #self.colors = np.array([[204,0,0],[78,145,6],[196,160,0],[52,101,164],[6,152,154],[239,41 ,41],[138,226,52],[253,233,79],[114,159,207],[173,127,168],[52 ,226,226],[238,238,238]])
        self.colors = np.array([[204,0,0],[78,145,6],[196,160,0],[52,101,164],[6,152,154],[239,41 ,70],[170,226,52],[253,233,100],[114,159,207],[173,127,168],[52 ,226,226],[238,238,238]])
        self.color_length = len(self.colors)

        self.brightness = self.colors[:,0]*0.299+self.colors[:,1]*0.587+self.colors[:,2]*0.114
        self.brightness_divisor = self.brightness/8

        self.colors_hue = self.colors.astype(np.float64)

        for i in range(self.color_length):
            #self.colors_hue[i] = self.colors_hue[i]/np.mean(self.colors_hue[i])
            self.colors_hue[i] = self.colors_hue[i]/self.brightness[i]

        self.color_chars=[]
        for i in range(self.char_length):
            tmp=[]
            for j in range(self.color_length):
                tmp.append(char_add_color(self.chars[i],j))
            self.color_chars.append(tmp)

        self.norm_matrix = np.zeros((self.strh,self.strw,3))
        self.color_img_matrix = np.zeros((self.color_length,self.strh,self.strw,3))
        self.color_contrast_matrix = np.zeros((self.color_length,self.strh,self.strw,3))
        for i in range(self.color_length):
            self.color_contrast_matrix[i,:,:] = self.colors_hue[i]
        self.color_contrast_distance = np.zeros((self.color_length,self.strh,self.strw))
    
    def blank(self,string):
        if self.sch>self.strh:
            for i in range((self.sch-self.strh)//2):
                string = '\n'+string+'\n'
        return string

    def gray(self,img):
        img = cv2.resize(img,(self.strw,self.strh),interpolation=cv2.INTER_AREA)
        if img.ndim == 3:
            if img.shape[2] == 4:
                img = img[:,:,:2]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        string = ''
        for i in range(self.strh):
            for j in range(self.strw):
                string += self.chars[img[i][j]//32]
            if i != self.strh-1:
                string += '\n'
        string = self.blank(string)

        return string


    def pixel_color(self,Y,dis):
        if Y<32:
            return ' '

        # color
        color_num = np.where(dis==np.min(dis))[0][0]

        # brightness
        #Y = pixel[0]*0.299+pixel[1]*0.587+pixel[2]*0.114
        brightness_level = int(Y/self.brightness_divisor[color_num])
        if brightness_level>8:
            brightness_level = 8

        char = self.color_chars[brightness_level][color_num]
        return char

    def color(self,img):
        img = cv2.resize(img,(self.strw,self.strh),interpolation=cv2.INTER_AREA)
        if img.shape[2] == 4:
            img = img[:,:,:2]
        img = img[:,:,::-1]
        img = img.astype(np.float64)
        img = np.clip(img, 1, 255)

        # get color distance matrix

        bright = img[:,:,0]*0.299+img[:,:,1]*0.587+img[:,:,2]*0.114
        for i in range(3):self.norm_matrix[:,:,i] = bright
        self.color_img_matrix[:] = img/self.norm_matrix

        # for i in range(3):self.norm_matrix[:,:,i] = np.mean(img,axis=2)
        # self.color_img_matrix[:] = img/self.norm_matrix

        self.color_contrast_distance = np.linalg.norm(self.color_img_matrix-self.color_contrast_matrix,ord=self.ord,axis=3)

        string = ''
        for i in range(self.strh):
            for j in range(self.strw):
                string += self.pixel_color(bright[i,j],self.color_contrast_distance[:,i,j])
            if i != self.strh-1:
                string += '\n'

        string = self.blank(string)

        return string
    
    def convert(self,img,isgray):
        if isgray:
            return self.gray(img)
        else :
            return self.color(img)

    def eval_performance(self,isgray):
        t1 = time.time()
        img = cv2.imread('./imgs/logo.png')
        print(self.convert(img,isgray))
        for i in range(10):
            img = cv2.imread('./imgs/test.jpg')
            img = cv2.resize(img,(1280,720))
            self.convert(img,isgray)
        t2 = time.time()
        recommend_fps = int(1/((t2-t1)/10))-1
        return recommend_fps

def main():
    pass

if __name__ == '__main__':
    main()
