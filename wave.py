#!/usr/bin/python
#coding=utf-8
'''
Created on 2011-7-2

@author: Chine
'''

import math
from PIL import Image

def wave(img, degree):
    '''
    @效果：波浪，对图像进行波浪特效处理
    @param img: instance of Image
    @param degree: 表示波浪的大小[0, 32] 
    @return: instance of Image
    '''
    
    degree = min(max(0, degree), 32)
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    width, height = img.size    
    pix = img.load()
    
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    pi2 = math.pi * 2
    
    for w in xrange(width):
        for h in xrange(height):
            x = int(degree * math.sin(pi2 * h / 128.0)) + w
            y = int(degree * math.cos(pi2 * w / 128.0)) + h
            
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            
            dst_pix[w, h] = pix[x, y]
    
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.realpath(__file__) + os.sep.join(['', 'images', 'lam.jpg'])

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
    img = wave(img, degree)
    img.save(os.path.splitext(path)[0]+'.wave.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)
