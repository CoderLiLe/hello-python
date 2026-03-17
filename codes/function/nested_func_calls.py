#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nested Func Calls
Python代码示例
"""

def test1():

    print("*" * 50)
    print("test 1")
    print("*" * 50)

def test2():

    print("-" * 50)
    print("test 2")

    # 函数的嵌套调用
    test1()

    print("-" * 50)

test2()
