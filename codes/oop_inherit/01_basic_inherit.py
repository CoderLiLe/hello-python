class A(object):
    def __init__(self):
        self.num = 1

    def info_print(self):
        print(self.num)


class B(A):
    pass


result = B()
result.info_print()
