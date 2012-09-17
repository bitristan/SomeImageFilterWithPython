#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-30

@author: Chine
'''

from PIL import Image

def ice(img):
    '''
    @效果：冰冻
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
            
            pix[w, h] = min(255, int(abs(r - g - b) * 3 / 2)), \
                        min(255, int(abs(g - b - r) * 3 / 2)), \
                        min(255, int(abs(b - r - g) * 3 / 2))
            
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = ice(img)
    img.save(os.path.splitext(path)[0]+'.ice.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)