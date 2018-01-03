#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on : 2017-12-29
#  Author : Joe Aaron
#  Email :  pant333@163.com
#  Description :  Real-time pedestrian detection
#  Souce :  From Yang Bincheng
############################################################
import cv2

cap = cv2.VideoCapture("pedestrian.avi")

while(1):
    #get a frame
    ret, frame = cap.read()
    #show a frame
    cv2.imshow("capture", frame)
    #model = cv2.creatGaussianBGModel(frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break