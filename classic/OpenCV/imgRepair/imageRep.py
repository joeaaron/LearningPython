#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on : 2018-7-31
#  Author : Joe Aaron
#  Email :  pant333@163.com
#  Description : 如何用python拯救一幅拍摄失败的图片？
#  https://zhuanlan.zhihu.com/p/28644779?utm_source=ZHShareTargetIDMore&utm_medium=social&utm_oi=37105992466432
############################################################
from __future__ import print_function

import matplotlib.pyplot as plt
from skimage import io
from skimage import exposure

image=io.imread('ori.jpg')

# 看看图片的类型，io.imread读取的过程，实际上将image转化成数组的形式
print(type(image)) #<class 'numpy.ndarray'>
# 此时，可以打印出图片看一看,打开的图片也就是第一张大家看到的原图
plt.imshow(image)

#exposure.histogram
hist,bin_center=exposure.histogram(image)
# bin_center为横轴,hist记录直方图的纵轴
fig,ax=plt.subplots(ncols=1)
ax.fill_between(bin_center,hist)

# 这里用到python中直方图均衡化函数 exposure.equalize_hist
equalization=exposure.equalize_hist(image)
hist,bin_centers=exposure.histogram(equalization)
fig,ax=plt.subplots(ncols=1)
#我们再看看equalize后的直方图
ax.fill_between(bin_centers,hist)
plt.imshow(equalization)
#赶紧保存吧
io.imsave('IMG_1634_mdf1.jpg',image)

#当然，我们也可以看看各个颜色通道的直方图分布
Rhist,Rbin_centers=exposure.histogram(equalization[:,:,0])#红色通道直方图
Ghist,Gbin_centers=exposure.histogram(equalization[:,:,1])#绿色通道直方图
Bhist,Bbin_centers=exposure.histogram(equalization[:,:,2])#蓝色通道直方图
fig,(ax_r,ax_g,ax_b)=plt.subplots(ncols=3,figsize=(10,5))
ax_r.fill_between(Rbin_centers,Rhist)
ax_g.fill_between(Gbin_centers,Ghist)
ax_b.fill_between(Bbin_centers,Bhist)

#复古图首先要去掉RGB通道，将整个画面改成灰色
#python中skimage.color.rgb2gray()函数可达到效果
gray_img=skimage.color.rgb2gray(image)
plt.imshow(gray_img,cmap="gray")
hist, bin_centers = exposure.histogram(image)

#更改对比度范围，让颜色变得更加鲜亮
img_intensity=skimage.exposure.rescale_intensity(gray_img,in_range=(0.2,0.55))
plt.imshow(img_intensity,cmap="gray")
io.imsave('IMG_1634_mdf2.jpg',img_intensity)