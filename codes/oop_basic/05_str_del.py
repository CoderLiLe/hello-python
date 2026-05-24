class Washer():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return '这是海尔洗衣机的说明书'

    def __del__(self):
        print(f'{self}对象已经被删除')


haier1 = Washer(10, 20)
print(haier1)
del haier1
