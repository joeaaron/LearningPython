#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-04-25
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。
############################################################
from PIL import Image, ImageDraw, ImageFont

def add_num(img):
    draw = ImageDraw.Draw(image)
    myfont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=40)
    fillcolor = "#ff0000"
    width, height = img.size
    draw.text((width-40, 0), '77', font=myfont, fill=fillcolor)
    img.save('./images/0000/result.jpg','jpeg')
    
    return 0

if __name__ == '__main__':
    image = Image.open('./images/0000/portrait.jpg')
    add_num(image)
