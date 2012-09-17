#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-3

@author: Chine
'''

from PIL import Image

def inosculate(bg_img, fg_img, transparency):
    '''
    @效果：图像融合
    @param bg_img: 背景图像
    @param fg_img: 前景图像
    @param transparency: 前景透明度  
    @return: instance of Image
    '''
    
    # 宽和高取两个图像宽和高的最小值
    width, height = tuple(map(min, zip(bg_img.size, fg_img.size)))
    
    if fg_img.mode != "RGBA":
        fg_img = fg_img.convert("RGBA")
    
    dst_img = Image.new("RGBA", (width, height))
    
    bg_pix = bg_img.load()
    fg_pix = fg_img.load()
    
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            if fg_pix[w, h][3] != 0:
                # 如果前景像素点不透明
                
                # pixel = FG * transparency / 255 + BG * (255 - transparency) / 255
                dst_pix[w, h] = tuple(
                                      [int((f - b) * transparency / 255 + b) 
                                       for (b, f) in zip(bg_pix[w, h], fg_pix[w, h])]
                                      )
            
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    bg_img_path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'guanlangaoshou.jpg'])
    fg_img_path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    transparency = 128
    
    if len(sys.argv) == 2:
        transparency = int(sys.argv[1])
    elif len(sys.argv) == 3:
        bg_img_path = sys.argv[1]
        fg_img_path = sys.argv[2]
    elif len(sys.argv) == 4:
        bg_img_path = sys.argv[1]
        fg_img_path = sys.argv[2]
        transparency = int(sys.argv[3])

    start = time.time()
    
    bg_img = Image.open(bg_img_path)
    fg_img = Image.open(fg_img_path)
    img = inosculate(bg_img, fg_img, transparency)
    img.save(os.path.splitext(fg_img_path)[0]+'.inosculate.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)