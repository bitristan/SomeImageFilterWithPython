#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-1

@author: Chine
'''

import math
from PIL import Image

def spherize(img):
    '''
    @效果：球面，对图像进行球面特效处理
    @param img: instance of Image
    @return: instance of Image
    '''
    
    width, height = img.size
    
    mid_x = width / 2
    mid_y = height / 2
    max_mid_xy = max(mid_x, mid_y)
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    pix = img.load()
    
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            offset_x = w - mid_x
            offset_y = h - mid_y
            
            radian = math.atan2(offset_y, offset_x) # 角度，使用math.atan2(y, x)求
            # 这里不是真正的半径
            radius = (offset_x ** 2 + offset_y ** 2) / max_mid_xy
            
            x = int(radius * math.cos(radian)) + mid_x
            y = int(radius * math.sin(radian)) + mid_y
            
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = spherize(img)
    img.save(os.path.splitext(path)[0]+'.spherize.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)