#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Gun():
    def __init__(self, model):
        self.model = model
        self.bullet_count = 0

    def add_bullet(self, count):
        self.bullet_count += count

    def shoot(self):
        if self.bullet_count <= 0:
            print("[%s]没有子弹了" % self.model)
            return
        self.bullet_count -= 1
        print("[%s] 突突突...[%s]" % (self.model, self.bullet_count))


class Soldier():
    def __init__(self, name):
        self.name = name
        self.gun = None

    def fire(self):
        if self.gun == None:
            print("[%s]还没有枪..." % self.name)
            return
        print("冲啊...[%s]" % self.name)
        self.gun.add_bullet(50)
        self.gun.shoot()


ak47 = Gun("AK47")

xsd = Soldier("许三多")
xsd.gun = ak47
xsd.fire()
print(xsd.gun)
