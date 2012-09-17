#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-27

@author: Chine
'''
from PIL import Image

from utils import Img2bin_arr, bin_arr2Img

def paper_cut(img, threshold, bg_color, fg_color):
    '''
    @效果：剪纸
    @param img: instance of Image
    @param threshold: 大小范围[0, 255]
    @param bg_color: 背景色，元组类型，格式：(L)（灰度）,(R, G, B)，或者(R, G, B, A)
    @param fg_color: 前景色
    @return: instance of Image
    '''
    matrix = Img2bin_arr(img, threshold) # 位图转化为二维二值数组
    return bin_arr2Img(matrix, bg_color, fg_color) # 二维二值数组转化为位图

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'niu.jpg'])
    threshold = 100
    bg_color = (255, 255, 255, 0)
    fg_color = (255, 0, 0, 255)
    
    if len(sys.argv) >= 2:
        path  = sys.argv[1]
    if len(sys.argv) == 3:
        threshold = int(sys.argv[2])
    if len(sys.argv) == 5:
        bg_color = tuple(sys.argv[3])
        fg_color = tuple(sys.argv[4])

    start = time.time()
    
    img = Image.open(path)
    img = paper_cut(img, threshold, bg_color, fg_color)
    img.save(os.path.splitext(path)[0]+'.papercut.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start) 