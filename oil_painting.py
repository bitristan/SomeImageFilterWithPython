#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-23

@author: Chine
'''
from PIL import Image

def oil_painting(img, brush_size, roughness):
    '''
    @效果：油画
    @param img: instance of Image
    @param brush_size: 笔刷大小，实际上为对当前像素点进行计算的范围 ，大小范围：[1, 8]
    @param roughness: 粗糙值，大小范围：[1, 255]
    @return: instance of Image
    
    @注意：此方法速度较慢
    '''
    
    if brush_size < 1: brush_size = 1
    if brush_size > 8: brush_size = 8
    
    if roughness < 1: roughness = 1
    if roughness > 255: roughness = 255
    
    width, height = img.size
    
    gray_img = img.convert("L") # 进行灰度预处理
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    dst_img = Image.new("RGBA", (width, height)) # 目标图片
    
    gray_pix = gray_img.load()
    pix = img.load()
    dst_pix = dst_img.load()
    
    arr_len = roughness + 1
    count = [0 for i in xrange(arr_len)]
    A = [0 for i in xrange(arr_len)]
    R = [0 for i in xrange(arr_len)]
    G = [0 for i in xrange(arr_len)]
    B = [0 for i in xrange(arr_len)]

    def reset():
        # 将count, A, R, G, B元素重置0
        for arr in (count, A, R, G, B):
            for i in xrange(arr_len):
                arr[i] = 0
    
    # 主计算过程
    # 计算当前像素点的brush_size宽度范围内
    # (灰度值 * 粗糙度 / 255)出现最多的像素点
    # 并计算出这些像素点的A, R, G, B平均值值
    # 以达到油画效果
    for w in xrange(width):
        left = w - brush_size
        if left < 0:
            left = 0
            
        right = w + brush_size
        if right > width - 1:
            right = width - 1
            
        for h in xrange(height):
            top = h - brush_size
            if top < 0:
                top = 0
                
            bottom = h + brush_size
            if bottom > height - 1:
                bottom = height - 1
                
            reset()
            
            for i in xrange(left, right+1):
                for j in xrange(top, bottom+1):
                    intensity = int(gray_pix[i, j] * roughness / 255)
                    count[intensity] += 1
                    p = pix[i, j]
                    A[intensity] += p[3]
                    R[intensity] += p[0]
                    G[intensity] += p[1]
                    B[intensity] += p[2]
            
            max_ins_count = max(count)
            max_idx = count.index(max_ins_count)
            
            dst_pix[w, h] = int(R[max_idx] / max_ins_count), \
                            int(G[max_idx] / max_ins_count), \
                            int(B[max_idx] / max_ins_count), \
                            int(A[max_idx] / max_ins_count)
                            
    return dst_img
    
if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    brush_size = 6
    roughness = 200
    
    if len(sys.argv) >= 3:
        brush_size = int(sys.argv[1])
        roughness = int(sys.argv[2])
    if len(sys.argv) == 4:
        path = sys.argv[3]

    start = time.time()
    
    img = Image.open(path)
    img = oil_painting(img, brush_size, roughness)
    img.save(os.path.splitext(path)[0]+'.oilpainting.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)