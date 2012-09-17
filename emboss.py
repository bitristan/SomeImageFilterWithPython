#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-6-24

@author: Chine
'''
from PIL import Image

from utils import Matrix33

def emboss(img):
    '''
    @效果：浮雕
    @param img: instance of Image
    @return: instance of Image
    
    @不推荐使用，PIL已经内置浮雕的滤镜处理
    '''
    
    # 要进行卷积转换的3×3矩阵
    matrix33 = [[-1, 0, -1],
                [0, 4, 0],
                [-1, 0, -1]]
    m = Matrix33(matrix33, offset=127)
    return m.convolute(img) # 进行卷积转换

if __name__ == "__main__":
    import sys, os, time
    
    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    
    if len(sys.argv) > 1:
        path = sys.argv[1]

    start = time.time()
    
    img = Image.open(path)
    img = emboss(img)
    img.save(os.path.splitext(path)[0]+'.emboss.jpg', 'JPEG')

    end = time.time()
    print 'It all spends %f seconds time' % (end-start)
    
'''
    from PIL import ImageFilter
    
    start = time.time()
    
    img = Image.open(path)
    img = img.filter(ImageFilter.EMBOSS)
    img.save(os.path.splitext(path)[0]+'.emboss2.jpg', 'JPEG')
    
    end = time.time()
    print 'It all spends %f seconds time' % (end-start)
'''