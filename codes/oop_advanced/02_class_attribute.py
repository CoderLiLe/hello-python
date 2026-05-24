class Dog(object):
    tooth = 10

    def __init__(self):
        self.age = 5

    def info_print(self):
        print(self.age)


wangcai = Dog()
xiaohei = Dog()

print(Dog.tooth)
print(wangcai.tooth)
print(xiaohei.tooth)

Dog.tooth = 12
print(Dog.tooth)
print(wangcai.tooth)
print(xiaohei.tooth)

wangcai.tooth = 20
print(Dog.tooth)
print(wangcai.tooth)
print(xiaohei.tooth)

print(wangcai.age)
wangcai.info_print()
