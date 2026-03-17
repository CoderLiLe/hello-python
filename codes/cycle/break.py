#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Break
Python代码示例
"""

i = 0
while i < 10:
    # break 某一条件满足时，退出循环，不再执行后续重复的代码
    # i == 3
    if i == 3:
        break
    print(i)
    i += 1

print("over")
