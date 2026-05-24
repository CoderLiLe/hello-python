class Washer():
    def print_info(self):
        print(f'洗衣机的宽度是{self.width}')
        print(f'洗衣机的高度是{self.height}')


haier1 = Washer()
haier1.width = 500
haier1.height = 800
haier1.print_info()
