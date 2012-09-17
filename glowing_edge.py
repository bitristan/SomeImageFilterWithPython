#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-8

@author: Chine
'''

import math
from PIL import Image

def glowing_edge(img):
    '''
    @效果：照亮边缘
    @param img: instance of Image
    @return: instance of Image
    '''
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        
    width, height = img.size
    pix = img.load()
    
    for w in xrange(width-1):
        for h in xrange(height-1):
            bottom = pix[w, h+1] # 下方像素点
            right = pix[w+1, h] # 右方像素点
            current = pix[w, h] # 当前像素点
            
            # 对r, g, b三个分量进行如下计算
            # 以r分量为例：int(2 * math.sqrt((r[current]-r[bottom])^2 + r[current]-r[right])^2))
            pixel = [int(math.sqrt((item[0] - item[1]) ** 2 + (item[0] - item[2]) ** 2) * 2) 
                     for item in zip(current, bottom, right)[:3]]
            pixel.append(current[3])
            
            pix[w, h] = tuple([min(max(0, i), 255) for i in pixel]) # 限制各分量值介于[0, 255]
            
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = glowing_edge(img)
    img.save(os.path.splitext(path)[0]+'.glowing_edge.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)
            