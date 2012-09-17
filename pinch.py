#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-1

@author: Chine
'''

import math
from PIL import Image

def pinch(img, degree, center=None):
    '''
    @效果：挤压，对图像进行挤压特效处理
    @param img: instance of Image
    @param degree: 表示挤压程度，大小[1, 32]
    @param center: 二元组(x, y)，表示挤压的中心点 ，默认为中心点(width/2, height/2)
    @return: instance of Image
    '''
    
    degree = min(max(1, degree), 32) # 限制degree的大小
    if img.mode != "RBGA":
        img = img.convert("RGBA")
    
    width, height = img.size
    if center is None:
        center = width / 2, height / 2 # 中心点
    
    pix = img.load()
    
    # 生成新的图像
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            # 当前像素点的偏移量
            offset_x, offset_y = w - center[0], h - center[1]
            
            radian = math.atan2(offset_y, offset_x) # 角度，用math.atan2(y, x)求出
            radius = math.sqrt(offset_x ** 2 + offset_y ** 2) # 当前像素点距离挤压点的距离
            
            # 半径越大，挤压的效果越不明显，选用开根模拟
            # 这里还要乘以权重
            act_radius = math.sqrt(radius) * degree 
            # 实际的像素点
            x = int(act_radius * math.cos(radian)) + center[0] 
            y = int(act_radius * math.sin(radian)) + center[1]
            
            # 约束x, y的大小
            x = min(max(0, x), width - 1)
            y = min(max(0, y), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    degree = 25
    
    if len(sys.argv) >= 2:
        try:
            degree = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    if len(sys.argv) == 3:
        path = sys.argv[1]
        degree = int(sys.argv[2])
    if len(sys.argv) == 4:
        center = int(sys.argv[2]), int(sys.argv[3])
    if len(sys.argv) == 5:
        degree = int(sys.argv[2])
        center = int(sys.argv[3]), int(sys.argv[4])

    start = time.time()
    
    img = Image.open(path)
    img = pinch(img, degree)
    img.save(os.path.splitext(path)[0]+'.pinch.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)