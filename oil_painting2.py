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
    
    @注意：达到和oil_painting.py几乎一致的效果
    @计算时间更长，主要目标是用更加简洁且Pythonic的代码方法书写
    '''
    if brush_size < 1: brush_size = 1
    if brush_size > 8: brush_size = 8
    
    if roughness < 1: roughness = 1
    if roughness > 255: roughness = 255
    
    width, height = img.size
    
    def L(p):
        '''
        @计算某个像素点p的灰度值
        @为了加快计算速度，没有再用img.convert('L')生成一个灰度图
        '''
        l = p[0] * 299/1000 + p[1] * 587/1000 + p[2] * 114/1000
        return int(l)
        
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    dst_img = Image.new("RGBA", (width, height)) # 目标图片
    
    pix = img.load()
    dst_pix = dst_img.load()
    
    # 主计算过程
    # 计算当前像素点的brush_size宽度范围内
    # (灰度值 * 粗糙度 / 255)出现最多的像素点
    # 并计算出这些像素点的A, R, G, B平均值值
    # 以达到油画效果
    for w in xrange(width):
        left = max(w - brush_size, 0)
        right = min(w + brush_size, width - 1)
            
        for h in xrange(height):
            top = max(h - brush_size, 0)
            bottom = min(h + brush_size, height - 1)

            intensity = lambda p: int(L(p) * roughness / 255)
            iter = groupby(
                           (pix[i, j] for j in xrange(top, bottom+1) for i in xrange(left, right+1)),
                           intensity
                           )
            result = max((g for g in iter.values()), key=len)
            RGBA = map(lambda l: int(sum(l) / len(l)), zip(*result))
            
            dst_pix[w, h] = tuple(RGBA)
                            
    return dst_img

def groupby(iterable, func):
    '''
    @对可迭代对象iterable里的每个元素item进行func(item)的操作
    @返回值字典
    @它将值相同的对象的值作为字典的键，将相同的对象以list的形式作为值
    @param iterable：可迭代对象
    @param func：计算函数
    '''
    results = {}
    for item in iterable:
        result = func(item)
        if result in results:
            results[result].append(item)
        else:
            results[result] = [item, ]
    return results
    
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
    img.save(os.path.splitext(path)[0]+'.oilpainting2.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)