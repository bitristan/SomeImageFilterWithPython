#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-30

@author: Chine
'''

import math
from PIL import Image

def whim(img):
    '''
    @效果：怪调
    @param img: instance of Image
    @return: instance of Image
    '''
    
    if img.mode != "RGB":
        img.convert("RGB")
    
    width, height = img.size
    pix = img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            r, g, b = pix[w, h]
            
            pix[w, h] = int(math.sin(math.atan2(g, b)) * 255), \
                        int(math.sin(math.atan2(b, r)) * 255), \
                        int(math.sin(math.atan2(r, g)) * 255)
            
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'guanlangaoshou.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = whim(img)
    img.save(os.path.splitext(path)[0]+'.whim.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)