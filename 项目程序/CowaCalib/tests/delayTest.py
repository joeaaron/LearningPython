#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
def demo(id):
    for i in range(0, 3):
        print id[i]


if __name__ == '__main__':
    demo([0, 1, 3])
    time.sleep(5)
    demo([0, 1, 7])