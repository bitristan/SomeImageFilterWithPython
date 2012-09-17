#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-7

@author: Chine
'''

import math
from PIL import Image

from adjustment import invert
from utils import Matrix33

def find_edge(img, angle):
    '''
    @效果：查找边缘
    @param img: instance of Image
    @param angle: 角度，大小[0, 360] 
    @return: instance of Image
    '''
    
    radian = angle * 2.0 * math.pi / 360.0
    
    pi4 = math.pi / 4.0
    
    matrix33 = [
        [int(math.cos(radian + pi4) * 256),
         int(math.cos(radian + 2.0 * pi4) * 256),
         int(math.cos(radian + 3.0 * pi4) * 256)],
        [int(math.cos(radian) * 256),
         0,
         int(math.cos(radian + 4.0 * pi4) * 256)],
        [int(math.cos(radian - pi4) * 256),
         int(math.cos(radian - 2.0 * pi4) * 256),
         int(math.cos(radian - 3.0 * pi4) * 256)]
        ]
    
    m = Matrix33(matrix33, scale=256)
    
    img = m.convolute(img) # 对图像进行3*3卷积转换
    
    return invert(img) # 对图像进行负像处理

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
    img = find_edge(img, angle)
    img.save(os.path.splitext(path)[0]+'.find_edge.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)