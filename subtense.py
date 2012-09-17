#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-30

@author: Chine
'''

from PIL import Image

def subtense(img):
    '''
    @效果：对调
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
            
            pix[w, h] = min(255, int(g * b / 255)), \
                        min(255, int(b * r / 255)), \
                        min(255, int(r * g / 255))
                  
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = subtense(img)
    img.save(os.path.splitext(path)[0]+'.subtense.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)