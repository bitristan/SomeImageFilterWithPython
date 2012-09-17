#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-24

@author: Chine
'''
import math
from PIL import Image

from utils import Matrix33

def relief(img, angle):
    '''
    @效果：彩色浮雕
    @param img: instance of Image
    @param angle: 进行卷积运算使用的其实偏移角度，大小范围[0, 360]
    @return: instance of Image
    '''
    if angle < 0: angle = 0
    if angle > 360: angle = 360

    radian = angle * math.pi / 180
    pi4 = math.pi / 4

    # 进行卷积转换的3×3矩阵
    matrix33 = [
        [int(math.cos(radian + pi4) * 256),
         int(math.cos(radian + 2 * pi4) * 256),
         int(math.cos(radian + 3 * pi4) * 256)],
        [int(math.cos(radian) * 256),
         256,
         int(math.cos(radian + 4 * pi4) * 256)],
        [int(math.cos(radian - pi4) * 256),
         int(math.cos(radian - 2 * pi4) * 256),
         int(math.cos(radian - 3 * pi4) * 256)]
        ]

    m = Matrix33(matrix33, scale=256) # 缩放值256

    return m.convolute(img)

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    angle = 60
    
    if len(sys.argv) == 2:
        try:
            angle = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        angle = int(sys.argv[2])

    start = time.time()
    
    img = Image.open(path)
    img = relief(img, angle)
    img.save(os.path.splitext(path)[0]+'.relief.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)