# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 2018
@author: JA
"""

import cv2
import numpy as np

def detect(image_name):
    print("正在识别"+image_name+'...')
    #Load the image and convert it to grayscale
    image = cv2.imread(image_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # compute the Scharr gradient magnitude representation of the iamges
     gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
    gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
    # substract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    # blur and threhold the image
    # 这里(13,13)是kernel matrix size，自己可以改变看看识别效果
    blurred = cv2.blur(gradient, (13, 13))
    # 这里的阀值200,255也可以根据图片自定义
    (_, thresh) = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    # construct a closing kernel and apply it to the thresholded image
    # (20, 15)也是一个参数，用来获取需要的kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 15))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)
    # Find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one
    # ValueError: too many values to unpack (expected 2)
    (img,cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    # 原文这里使用cv2.cv.BoxPoints，新版本已经移除，换为cv2.boxPoints
    box = np.int0(cv2.boxPoints(rect))
    # draw a bounding box around the detected barcode
    # and display the image
    cv2.drawContours(image, [box], -1, (0,255,0), 3)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    print("Done...\n##################################")