#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class School(Master):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')
        super().__init__()
        super().make_cake()


class Prentice(School):
    def __init__(self):
        self.kongfu = '[独创煎饼果子技术]'

    def make_cake(self):
        self.__init__()
        print(f'运用{self.kongfu}制作煎饼果子')

    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)

    def make_old_cake(self):
        super().__init__()
        super().make_cake()


daqiu = Prentice()

daqiu.make_old_cake()
