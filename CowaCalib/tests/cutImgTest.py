#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pyscreenshot as ImageGrab

def RectCapturePlus(rect, filename, fmt = None):
    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
    sleep(1)
    win32api.keybd_event(win32con.VK_SNAPSHOT, 0, win32con.KEYEVENTF_KEYUP, 0)
    sleep(1)
    try:
        im = ImageGrab.grabclipboard()
        im = im.crop(rect)
        im.save(filename, fmt)
    except :
        return False
    return True
    
if __name__ == "__main__":
    # part of the screen
    im = ImageGrab.grab()
    im.show()