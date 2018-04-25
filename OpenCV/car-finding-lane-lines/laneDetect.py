#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on : 2017-02-12
#  Author : Joe Aaron
#  Email :  pant333@163.com
#  Description :  Detect the lanes of the road
############################################################
import matplotlib.pyplot as plt
import cv2
import os, glob, imageio
#imageio.plugins.ffmpeg.download()
import numpy as np
from collections import deque
from moviepy.editor import VideoFileClip

QUEUE_LENGTH = 50

class LaneDetector:
    def _init_(self):
        self.left_lines = deque(maxlen = QUEUE_LENGTH)
        self.right_lines = deque(maxlen = QUEUE_LENGTH)
            
    def mean_line(line, lines):
        if line is not None:
            lines.append(line)

        if len(lines)>0:
            line = np.mean(lines, axis=0, dtype=np.int32)
            line = tuple(map(tuple, line)) # make sure it's tuples not numpy array for cv2.line to work
        return line   
        
    def process(self,image):
        try:
            white_yellow = select_white_yellow(image)
            gray = convert_gray_scale(white_yellow)
            smooth_gray = apply_smoothing(gray)
            edges = detect_edges(smooth_gray)
            regions = select_region(edges)
            lines = hough_lines(regions)
            left_line, right_line = lane_lines(image, lines)

            left_line  = self.mean_line(left_line,  self.left_lines)
            right_line = self.mean_line(right_line, self.right_lines)

            return draw_lane_lines(image, (left_line, right_line))
        except:
            #traceback.print_exc()
            return draw_lane_lines(image, (left_line, right_line))
            
def show_images(images, cmap=None):
    cols = 2
    rows = (len(images)+1)//cols
    
    plt.figure(figsize=(10, 11))
    for i, image in enumerate(images):
        plt.subplot(rows, cols, i+1)
        # use gray scale color map if there is only one channel
        cmap = 'gray' if len(image.shape)==2 else cmap
        plt.imshow(image, cmap=cmap)
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.show()

# image is expected be in RGB color space
def select_white_yellow(image): 
    converted = convert_hls(image)
    # white color mask
    lower = np.uint8([0, 200, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(converted, lower, upper)
    # yellow color mask
    lower = np.uint8([10, 0, 100])
    upper = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(converted, lower, upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    masked = cv2.bitwise_and(image, image, mask = mask)
    return masked
	
def convert_hls(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    
def convert_gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
def apply_smoothing(image, kernel_size=15):
    """
    kernel_size must be postivie and odd
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
def detect_edges(image, low_threshold=50, high_threshold=150):
    return cv2.Canny(image, low_threshold, high_threshold)
    
def filter_region(image, vertices):
    """
    Create the mask using the vertices and apply it to the input image
    """
    mask = np.zeros_like(image)
    if len(mask.shape) == 2:
        cv2.fillPoly(mask, vertices, 255)
    else:
         cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension        
    return cv2.bitwise_and(image, mask)
    
def select_region(image):
    """
    It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    """
    #first, define the polygon by vertices
    rows, cols = image.shape[:2]
    bottom_left  = [cols*0.1, rows*0.95]
    top_left     = [cols*0.4, rows*0.6]
    bottom_right = [cols*0.9, rows*0.95]
    top_right    = [cols*0.6, rows*0.6] 
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return filter_region(image, vertices)

def hough_lines(image):
    """
    `image` should be the output of a Canny transform.
    
    Returns hough lines (not the image with lines)
    """

    plines = cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)
    return plines

def draw_lines(image, lines, color=[255, 0, 0], thickness=2, make_copy=True):
    # the lines returned by cv2.HoughLinesP has the shape (-1, 1, 4)
    if make_copy:
        image = np.copy(image) # don't want to modify the original
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
    return image

def average_slope_intercept(lines):
    left_lines    = [] # (slope, intercept)
    left_weights  = [] # (length,)
    right_lines   = [] # (slope, intercept)
    right_weights = [] # (length,)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x2==x1:
                continue # ignore a vertical line
            slope = (float(y2-y1)/(x2-x1))
            intercept = y1 - slope*x1
            length = np.sqrt((y2-y1)**2+(x2-x1)**2)
            if slope < 0: # y is reversed in image
                left_lines.append((slope, intercept))
                left_weights.append((length))
            else:
                right_lines.append((slope, intercept))
                right_weights.append((length))
    
    # add more weight to longer lines    
    left_lane  = np.dot(left_weights,  left_lines) /np.sum(left_weights)  if len(left_weights) >0 else None
    right_lane = np.dot(right_weights, right_lines)/np.sum(right_weights) if len(right_weights)>0 else None
    
    return left_lane, right_lane # (slope, intercept), (slope, intercept)

def make_line_points(y1, y2, line):
    """
    Convert a line represented in slope and intercept into pixel points
    """
    if line is None:
        return None
    
    slope, intercept = line
    
    # make sure everything is integer as cv2.line requires it
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    y1 = int(y1)
    y2 = int(y2)
    
    return ((x1, y1), (x2, y2))

def lane_lines(image, lines):
    left_lane, right_lane = average_slope_intercept(lines)
    
    y1 = image.shape[0] # bottom of the image
    y2 = y1*0.6         # slightly lower than the middle

    left_line  = make_line_points(y1, y2, left_lane)
    right_line = make_line_points(y1, y2, right_lane)
    
    return left_line, right_line
    
def draw_lane_lines(image, lines, color=[255, 0, 0], thickness= 20):
    # make a separate image to draw lines and combine with the orignal later
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            #line[0] first point, line[1] second point
            cv2.line(line_image, line[0], line[1], color, thickness)
            cv2.imshow('demo', line_image)
            cv2.waitKey(0)
    # image1 * α + image2 * β + λ
    # image1 and image2 must be the same shape.
    return cv2.addWeighted(image, 1.0, line_image, 0.95, 0.0)
             
def process_video(video_input, video_output):
    detector = LaneDetector()

    clip = VideoFileClip(os.path.join('test_videos', video_input))
    processed = clip.fl_image(detector.process)
    processed.write_videofile(os.path.join('output_videos', video_output), audio=False)
    
def process(image):
    white_yellow = select_white_yellow(image)
    gray = convert_gray_scale(white_yellow)
    smooth_gray = apply_smoothing(gray)
    edges = detect_edges(smooth_gray)
    regions = select_region(edges)
    lines = hough_lines(regions)
    left_line, right_line = lane_lines(image, lines)

   # left_line  = self.mean_line(left_line,  self.left_lines)
   # right_line = self.mean_line(right_line, self.right_lines)

    lane_images = draw_lane_lines(image, (left_line, right_line))
    #show_images(lane_images)

#show_images(list(map(convert_hls, test_images)))
if __name__ == '__main__':
    test_images = [plt.imread(path) for path in glob.glob('test_images/*.jpg')]
    white_yellow_images = list(map(select_white_yellow, test_images))
    gray_images = list(map(convert_gray_scale, white_yellow_images))
    blurred_images = list(map(lambda image: apply_smoothing(image), gray_images))
    edge_images = list(map(lambda image: detect_edges(image), blurred_images))
    roi_images = list(map(select_region, edge_images))
    list_of_lines = list(map(hough_lines, roi_images))
    
    line_images = []
    for image, lines in zip(test_images, list_of_lines):
        line_images.append(draw_lines(image, lines))
    
    lane_images = []
    for image, lines in zip(test_images, list_of_lines):
        lane_images.append(draw_lane_lines(image, lane_lines(image, lines)))
        
    show_images(lane_images)
    
    # test_images = cv2.imread("solidWhiteCurve.jpg")
    # process(test_images)
    
    #process_video("solidYellowLeft.mp4", "white2.mp4")