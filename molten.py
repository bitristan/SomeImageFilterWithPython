#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-30

@author: Chine
'''

from PIL import Image

def molten(img):
    '''
    @效果：熔铸
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
            
            pix[w, h] = min(255, int(abs(r * 128 / (g + b + 1)))), \
                        min(255, int(abs(g * 128 / (b + r + 1)))), \
                        min(255, int(abs(b * 128 / (r + g + 1))))
            
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = molten(img)
    img.save(os.path.splitext(path)[0]+'.molten.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)