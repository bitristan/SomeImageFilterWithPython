#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-8

@author: Chine
'''

from PIL import Image

def mosaic(img, block_size):
    '''
    @效果：马赛克
    @param img: instance of Image
    @param block_size: 方块大小，范围[1, 32] 
    @return: instance of Image
    '''
    
    block_size = min(max(block_size, 1), 32)
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    width, height = img.size
    pix = img.load()
    
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    for w in xrange(0, width, block_size):
        for h in xrange(0, height, block_size):
            r_sum, g_sum, b_sum = 0, 0, 0
            size = block_size ** 2
            
            for i in xrange(w, min(w+block_size, width)):
                for j in xrange(h, min(h+block_size, height)):
                    r_sum += pix[i, j][0]
                    g_sum += pix[i, j][1]
                    b_sum += pix[i, j][2]
                    
            r_ave = int(r_sum / size)
            g_ave = int(g_sum / size)
            b_ave = int(b_sum / size)
            
            for i in xrange(w, min(w+block_size, width)):
                for j in xrange(h, min(h+block_size, height)):
                    dst_pix[i, j] = r_ave, g_ave, b_ave, pix[w, h][3]
                    
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    block_size = 10
    
    if len(sys.argv) == 2:
        try:
            block_size = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        block_size = int(sys.argv[2])

    start = time.time()
    
    img = Image.open(path)
    img = mosaic(img, block_size)
    img.save(os.path.splitext(path)[0]+'.mosaic.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)