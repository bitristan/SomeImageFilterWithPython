#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-6

@author: Chine
'''

import random
from PIL import Image

def diffuse(img, degree):
    '''
    @效果：扩散
    @param img: instance of Image
    @param degree: 扩散范围，大小[1, 32] 
    @return: instance of Image
    '''
    
    degree = min(max(1, degree), 32)
    
    width, height = img.size
    
    dst_img = Image.new(img.mode, (width, height))
    
    pix = img.load()
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            # 随机获取当前像素周围一随机点
            x = w + random.randint(-degree, degree)
            y = h + random.randint(-degree, degree)
            
            # 限制范围
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    degree = 16
    
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
    img = diffuse(img, degree)
    img.save(os.path.splitext(path)[0]+'.diffuse.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)