#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-2

@author: Chine
'''

import math
from PIL import Image

def swirl(img, degree):
    '''
    @效果：漩涡，对图像进行漩涡特效处理
    @param img: instance of Image
    @param degree: 表示漩涡的大小[0, 100] 
    @return: instance of Image
    '''
    degree = min(max(0, degree), 100) / 1000.0
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
        
    width, height = img.size
    pix = img.load()
    
    center = width / 2, height / 2 # 漩涡中心点就在图片中心
    
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            offset_x = w - center[0]
            offset_y = h - center[1]
            
            radian = math.atan2(offset_y, offset_x) # 角度，使用math.atan2(y, x)进行计算
            radius = math.sqrt(offset_x ** 2 + offset_y ** 2) # 半径，即像素点距中心距离
            
            # 距离越远，旋转的角度就越大
            # 新角度为：角度 + 距离 × 权重
            x = int(radius * math.cos(radian + radius * degree)) + center[0] 
            y = int(radius * math.sin(radian + radius * degree)) + center[1]
            
            x = min(max(0, x), width - 1)
            y = min(max(0, y), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    degree = 4
    
    if len(sys.argv) == 2:
        try:
            degree = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        degree = sys.argv[2]

    start = time.time()
    
    img = Image.open(path)
    img = swirl(img, degree)
    img.save(os.path.splitext(path)[0]+'.swirl.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)