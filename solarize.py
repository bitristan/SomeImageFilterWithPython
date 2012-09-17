#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-27

@author: Chine
'''

from PIL import Image

def solarize(img):
    '''
    @效果：曝光
    @param img: instance of Image
    @return: instance of Image
    '''
    if img.mode != "RGB":
        img = img.convert("RGB")
        
    return img.point(lambda i: i ^ 0xFF if i < 128 else i)

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = solarize(img)
    img.save(os.path.splitext(path)[0]+'.solarize.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start) 