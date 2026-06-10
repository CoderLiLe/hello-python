#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Dog(object):
    __tooth = 10

    @classmethod
    def get_tooth(cls):
        return cls.__tooth

    @staticmethod
    def info_print():
        print('这是一个狗类，用于创建狗实例....')


wangcai = Dog()
result = wangcai.get_tooth()
print(result)

wangcai.info_print()
Dog.info_print()
