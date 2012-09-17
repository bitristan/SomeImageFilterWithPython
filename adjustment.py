#!/usr/bin/env python
#coding=utf-8
'''
Created on 2011-7-7

@author: Chine
'''

from PIL import Image

def invert(img):
    '''对图像进行负像处理'''
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    width, height = img.size
    
    pix = img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            r, g, b, a = pix[w, h]
            pix[w, h] = r ^ 0xFF, \
                        g ^ 0xFF, \
                        b ^ 0xFF, \
                        a
    return img

def interleaving(img):
    '''交叉反转'''
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    width, height = img.size
    
    pix = img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            if (w + h) % 2 == 0:
                r, g, b, a = pix[w, h]
                pix[w, h] = r ^ 0xFF, \
                            g ^ 0xFF, \
                            b ^ 0xFF, \
                            a
    return img

def contrast(img, degree):
    '''
    @图像对比度调整
    @param img: instance of PIL Image
    @param degree: 对比度[-100, 100]  
    @return: instance of PIL Image
    '''
    
    degree = min(max(-100, degree), 100)
    
    _contrast = (degree + 100.0) / 100.0
    _contrast **= 2
    
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    
    width, height = img.size
    pix = img.load()
    
    for w in xrange(width):
        for h in xrange(height):
            r, g, b, a = pix[w, h]
            
            r = int(((r / 255.0 - 0.5) * _contrast + 0.5) * 255)
            g = int(((g / 255.0 - 0.5) * _contrast + 0.5) * 255)
            b = int(((b / 255.0 - 0.5) * _contrast + 0.5) * 255)
            
            r = min(max(r, 0), 255)
            g = min(max(g, 0), 255)
            b = min(max(b, 0), 255)
            
            pix[w, h] = r, g, b, a
            
    return img