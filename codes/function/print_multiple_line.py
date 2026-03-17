#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print Multiple Line
Python代码示例
"""

def print_line(char, times):

    print(char * times)


def print_lines(c, t):

    i = 0
    while i < 5:
        print_line(c, t)
        i += 1


print_lines("U", 20)
