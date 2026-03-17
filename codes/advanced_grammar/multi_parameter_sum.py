#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi Parameter Sum
Python代码示例
"""

import argparse


def sum_numbers(*args):

    num = 0
    # 循环遍历
    for n in args:
        num += n

    print(args)
    return num


res = sum_numbers(1, 2, 3, 4, 5)
print(res)
