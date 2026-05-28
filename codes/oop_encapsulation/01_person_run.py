#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Person():
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return "我的名字叫%s，体重是%.2f" % (self.name, self.weight)

    def run(self):
        print("%s 爱跑步，锻炼身体" % self.name)
        self.weight -= 0.5

    def eat(self):
        print("%s 是吃货，吃完这顿再减肥" % self.name)
        self.weight += 1


xm = Person("小明", 75)
xm.run()
xm.eat()
print(xm)
