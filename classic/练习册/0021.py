#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-05-29
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  
############################################################
"""
第 0021 题：
最小二乘法多项式拟合曲线
"""
import numpy as np 
from scipy.optimize import leastsq
import pylab as pl 

x = np.arange(1, 17, 1)
y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])

#第一个拟合，自由度为3
z1 = np.polyfit(x, y ,3)
# 生成多项式对象
p1 = np.poly1d(z1)
print(z1)
print(p1)
 
# 第二个拟合，自由度为6
z2 = np.polyfit(x, y, 6)
# 生成多项式对象
p2 = np.poly1d(z2)
print(z2)
print(p2) 
# 绘制曲线 
# 原曲线
pl.plot(x, y, 'b^-', label='Origin Line')
pl.plot(x, p1(x), 'gv--', label='Poly Fitting Line(deg=3)')
pl.plot(x, p2(x), 'r*', label='Poly Fitting Line(deg=6)')
pl.axis([0, 18, 0, 18])
pl.legend()
# Save figurepl.savefig('scipy02.png', dpi=96)