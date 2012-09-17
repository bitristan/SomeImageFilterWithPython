#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-24

@author: Chine
'''
from PIL import Image

def pencil(img, threshold):
    '''
    @效果：铅笔画
    @param img: instance of Image
    @param threshold: 阈值，阈值越小，绘制的像素点越多，大小范围[0, 100]
    @return: instance of Image
    '''
    if threshold < 0: threshold = 0
    if threshold > 100: threshold = 100

    width, height = img.size
    dst_img = Image.new("RGBA", (width, height))

    if img.mode != "RGBA":
        img = img.convert("RGBA")

    pix = img.load()
    dst_pix = dst_img.load()

    # 主方法
    # 主要将当前像素的R, G, B四个分量分别与周围的8个像素点的对应值的平均值比较
    # 如果都大于某阈值
    # 绘制该像素点，同时A分量等于当前像素点的alpha值即可
    for w in xrange(width):
        for h in xrange(height):
            if w == 0 or w == width - 1 \
               or h == 0 or h == height - 1:
                continue
            
            # 包含当前像素点的共九个像素点
            around_wh_pixels = [pix[i, j][:3] for j in xrange(h-1, h+2) for i in xrange(w-1, w+2)]
            # 排除当前像素点
            exclude_wh_pixels = tuple(around_wh_pixels[:4] + around_wh_pixels[5:])
            # 计算周围8个像素点的R, G, B分量平均值      
            RGB = map(lambda l: int(sum(l) / len(l)), zip(*exclude_wh_pixels))
            
            cr_p = pix[i, j] # 当前像素点

            cr_draw = all([abs(cr_p[i] - RGB[i]) >= threshold for i in range(3)])

            if cr_draw:
                dst_pix[w, h] = 0, 0, 0, cr_p[3]
            else:
                dst_pix[w, h] = 255, 255, 255, cr_p[3]

    return dst_img

if __name__ == "__main__":
    import sys, os, time

    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    threshold = 10
    
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
    img = pencil(img, threshold)
    img.save(os.path.splitext(path)[0]+'.pencil.png', 'PNG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)