#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-23

@author: Chine
'''
from PIL import Image

def sketch(img, threshold):
    '''
    @效果：素描
    @param img: instance of Image
    @param threshold: 阈值，阈值越小，绘制的像素点越多，大小范围[0, 100]
    @return: instance of Image
    '''
    if threshold < 0: threshold = 0
    if threshold > 100: threshold = 100
    
    width, height = img.size
    img = img.convert('L') # convert to grayscale mode
    pix = img.load() # get pixel matrix

    # 主计算方法
    # 根据经验，对当前像素点的灰度值与右下角比较
    # 差值大于阈值则绘制
    for w in xrange(width):
        for h in xrange(height):
            if w == width-1 or h == height-1:
                continue
            
            src = pix[w, h] # 当前像素点
            dst = pix[w+1, h+1] # 右下角像素点

            diff = abs(src - dst)

            if diff >= threshold:
                pix[w, h] = 0
            else:
                pix[w, h] = 255

    return img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    threshold = 15
    
    if len(sys.argv) == 2:
        try:
            threshold = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        threshold = int(sys.argv[2])
        
    start = time.time()
    
    img = Image.open(path)
    img = sketch(img, threshold)
    img.save(os.path.splitext(path)[0]+'.sketch.jpg', 'JPEG')
    
    end = time.time()
    print 'It all spends %f seconds time' % (end-start)