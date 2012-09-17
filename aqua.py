#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-29

@author: Chine
'''

from PIL import Image

def aqua(img):
    '''
    @效果：碧绿
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
            
            pix[w, h] = min(255, int((g - b) ** 2 / 128)), \
                        min(255, int((r - b) ** 2 / 128)), \
                        min(255, int((r - g) ** 2 / 128))
            
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = aqua(img)
    img.save(os.path.splitext(path)[0]+'.aqua.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)