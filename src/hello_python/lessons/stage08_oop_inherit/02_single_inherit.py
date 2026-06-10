#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class Prentice(Master):
    pass


daqiu = Prentice()
print(daqiu.kongfu)
daqiu.make_cake()
