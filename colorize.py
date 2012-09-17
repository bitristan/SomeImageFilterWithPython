#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-29

@author: Chine
'''

from PIL import Image

def colorize(img, red, green, blue):
    '''
    @效果：颜色渲染
    @param img: instance of Image
    @return: instance of Image
    '''
    
    red = max(0, red)
    red = min(255, red) 
    green = max(0, green)
    green = min(255, green)
    blue = max(0, blue)
    blue = min(255, blue)
    
    gray_img = img.convert("L")
        
    width, height = img.size
    pix = img.load()
    gray_pix = gray_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            gray = gray_pix[w, h]
            r, g, b = pix[w, h]
            
            r = int(red * gray / 255)
            g = int(green * gray /255)
            b = int(blue * gray /255)
            
            pix[w, h] = r, g, b
            
    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    red, green, blue = 250, 88, 244

    if len(sys.argv) == 2:
        path = sys.argv[1]
    elif len(sys.argv) == 5:
        path  = sys.argv[1]
        red = int(sys.argv[2])
        green = int(sys.argv[3])
        blue = int(sys.argv[4])
    elif len(sys.argv) == 4:
        red = int(sys.argv[1])
        green = int(sys.argv[2])
        blue = int(sys.argv[3])

    start = time.time()
    
    img = Image.open(path)
    img = colorize(img, red, green, blue)
    img.save(os.path.splitext(path)[0]+'.colorize.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)