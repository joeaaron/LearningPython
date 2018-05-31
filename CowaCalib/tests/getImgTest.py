#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def GetImgSaveByIdxPro(id, index):    
    if index < 5:
        for i in range(0, len(id)):
            dir = 'image/%d'%(id[i] + 1)
            print dir
            print id[i] + 0

        for i in range(0, len(id)):
            dir = 'image/%d'%(id[i] + 1)
            print dir
            print id[i] + 8
            
    elif index == 5:
        for i in range(0, len(id)):
            dir = 'image/%d'%(id[i] + 1)
            print dir
            print id[i] + 0
            
    elif index == 6:
        for i in range(0, len(id)):
            dir = 'image/%d'%(id[i] + 1)
            print dir
            print id[i] + 0
    return True

if __name__ == '__main__':
    for index in range(0, 7):
        GetImgSaveByIdxPro([1, 3], index)