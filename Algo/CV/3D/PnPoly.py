#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on : 2024-04-17
#  Author : Joe Aaron
#  Email :  pant333@163.com
#  Description : 实现判定一个点是否在封闭的多边形内。
#  Priciple:  由W. Randolph Franklin提出的，根据Jordan curve theorem，多边形将平面分为内外两个区域，
#             假设待测点在多边形内部，从待测点引出一条射线必然会与多边形有至少一个交点。
#             该射线与多边形第一次相交时将“冲出”多边形，第二次相交将“进入”多边形，
#             依此类推，若射线与多边形有奇数个交点，则该点在多边形内部，反之则在外部
############################################################

"""
  Check if a point is inside a polygon.

  Arguments:
  x -- x-coordinate of the point
  y -- y-coordinate of the point
  polygon -- list of tuples representing the vertices of the polygon

  Returns:
  True if the point is inside the polygon, False otherwise
"""
def Points_Inside_Polygon(x, y, polygon):
    n = len(polygon)
    inside = False

    # Create a ray form the point towards right and count intersections with the polygon
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        # 相似三角形，计算水平射线和多边形边交点的x坐标
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Example usage:
polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]  # Define a square polygon
point = (2, 5)  # Define a point to check
print(Points_Inside_Polygon(*point, polygon))  # Output: True