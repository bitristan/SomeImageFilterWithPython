#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-27

@author: Chine
'''

from PIL import Image

def comic(img):
    '''
    @效果：连环画
    @param img: instance of Image
    @return: instance of Image
    '''
    width, height = img.size
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    pix = img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            r, g, b = pix[w, h]
            
            pix[w, h] = tuple(map(lambda i: min(255, i),
                                  [abs(g - b + g + r) * r / 256,
                                   abs(b - g + b + r) * r / 256,
                                   abs(b - g + b + r) * r / 256]))
                
    return img.convert('L')

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'guanlangaoshou.jpg'])
    
    if len(sys.argv) == 2:
        path  = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = comic(img)
    img.save(os.path.splitext(path)[0]+'.comic.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)