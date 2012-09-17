#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-3

@author: Chine
'''

import math
from PIL import Image

from inosculate import inosculate

def moire_fringe(img, degree):
    '''
    @效果：摩尔纹，对图像进行摩尔纹特效处理
    @param img: instance of Image
    @param degree: 强度，大小范围[1, 16] 
    @return: instance of Image
    '''
    
    degree = min(max(degree, 1), 16)
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        
    width, height = img.size
    center = width / 2, height / 2 # 中心点
    pix = img.load()
    
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            offset_x = w - center[0]
            offset_y = h - center[1]
            
            radian = math.atan2(offset_y, offset_x) # 角度
            radius = math.sqrt(offset_x ** 2 + offset_y ** 2) # 半径
            
            x = int(radius * math.cos(radian + degree * radius))
            y = int(radius * math.sin(radian + degree * radius))
            
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return inosculate(img, dst_img, 128) # 对生成的图像和源图像进行色彩混合

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    degree = 6
    
    if len(sys.argv) == 2:
        try:
            degree = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        degree = sys.argv[2]

    start = time.time()
    
    img = Image.open(path)
    img = moire_fringe(img, degree)
    img.save(os.path.splitext(path)[0]+'.moire_fringe.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)