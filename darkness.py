#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-30

@author: Chine
'''

from PIL import Image

def darkness(img):
    '''
    @效果：暗调
    @param img: instance of Image
    @return: instance of Image
    '''
    
    return img.point(lambda i: int(i ** 2 / 255))

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = darkness(img)
    img.save(os.path.splitext(path)[0]+'.darkness.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)