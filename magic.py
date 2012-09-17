#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-10

@author: Chine
'''

from PIL import Image

from adjustment import interleaving, contrast
from inosculate import inosculate

def magic(bg_img, fg_img, transparency, _contrast):
    '''
    @效果：将两张图像合成为魔术图
    @param bg_img: 背景图像
    @param fg_img: 前景图像
    @param transparency: 前景透明度  [0, 255]
    @param _contrast: 前景图与背景图的对比度[-100, 100]
    @return: instance of Image
    '''
    
    bg_img = interleaving(bg_img)
    bg_img = contrast(bg_img, _contrast)
    
    return inosculate(bg_img, fg_img, transparency)

if __name__ == "__main__":
    import sys, os, time

    bg_img_path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'guanlangaoshou.jpg'])
    fg_img_path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    transparency = 128
    _contrast = -50
    
    if len(sys.argv) == 2:
        transparency = int(sys.argv[1])
    elif len(sys.argv) == 3:
        try:
            transparency = int(sys.argv[1])
            _contrast = int(sys.argv[2])
        except ValueError:
            bg_img_path = sys.argv[1]
            fg_img_path = sys.argv[2]
    elif len(sys.argv) == 5:
        bg_img_path = sys.argv[1]
        fg_img_path = sys.argv[2]
        transparency = int(sys.argv[3])
        _contrast = int(sys.argv[4])

    start = time.time()
    
    bg_img = Image.open(bg_img_path)
    fg_img = Image.open(fg_img_path)
    img = magic(bg_img, fg_img, transparency, _contrast)
    img.save(os.path.splitext(fg_img_path)[0]+'.magic.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)