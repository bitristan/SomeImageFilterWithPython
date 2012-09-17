#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-24

@author: Chine
'''
import operator
from PIL import Image

class Matrix33(object):
    '''
    @3×3矩阵
    @用来进行卷积转换
    '''
    def __init__(self, matrix33, scale=1, offset=0):
        '''
        @param matrix33: 3×3矩阵
        @param scale: 缩放比例
        @param offset: 偏移量
        '''
        self.matrix33 = matrix33
        self.scale = scale
        self.offset = offset

    def check(self):
        assert len(self.matrix33) == 3
        for l in self.matrix33:
            assert len(l) == 3

    def convolute(self, img):
        if self.scale == 0: self.scale = 1
        
        width, height = img.size

        if img.mode != "RGBA":
            img = img.convert("RGBA")
        pix = img.load()

        dst_img = Image.new("RGBA", (width, height))
        dst_pix = dst_img.load()

        for w in xrange(width):
            for h in xrange(height):
                if w == 0 or w == width-1 \
                   or h == 0 or h == height-1:
                    continue

                if pix[w, h][3] > 0:
                    # 不透明的时候才进行处理
                    t_dst = []
                    
                    # 分别对R, G, B三个分量进行计算
                    for idx in range(3):
                        # 将当前像素点周围九个元素的分量值分别与对应位置的3×3矩阵值相乘求和
                        p = reduce(
                            operator.add,
                            [pix[i, j][idx] * self.matrix33[j-h+1][i-w+1] \
                             for j in range(h-1, h+2) for i in range(w-1, w+2)]
                            )
                        p = p / self.scale + self.offset
                        p = max(0, p)
                        p = min(255, p)
                        t_dst.append(p)

                    dst_pix[w, h] = tuple(t_dst)

        return dst_img
    
def Img2bin_arr(img, threshold):
    '''
    @将位图流转化为二维二值数组
    @param img: instance of Image
    @param threshold: 大小范围[0, 255]
    '''
    threshold = max(0, threshold)
    threshold = min(255, threshold)
    
    if img.mode != 'L':
        img = img.convert('L')
        
    width, height = img.size
    pix = img.load()
    
    get_val = lambda p: 255 if p >= threshold else 0
        
    return [[get_val(pix[w, h]) for w in xrange(width)] for h in xrange(height)]

def bin_arr2Img(matrix, bg_color, fg_color):
    '''
    @将二维二值数组转化为位图流
    @param img: instance of Image
    @param bg_color: 背景色，元组类型，格式：(L)（灰度）,(R, G, B)，或者(R, G, B, A)
    @param fg_color: 前景色
    '''
    def ensure_color(color):
        if len(color) == 1:
            return (color, color, color, 255)
        elif len(color) == 3:
            color = list(color)
            color.append(255)
            return tuple(color)
        elif len(color) == 4:
            return color
        else:
            raise ValueError, 'len(color) cannot be %d' % len(color)
        
    bg_color = ensure_color(bg_color)
    fg_color = ensure_color(fg_color)
    
    height, width = len(matrix), len(matrix[0])
    dst_img = Image.new("RGBA", (width, height))
    dst_pix = dst_img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            if matrix[h][w] < 128:
                dst_pix[w, h] = fg_color
            else:
                dst_pix[w, h] = bg_color
                
    return dst_img