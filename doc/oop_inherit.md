# 面向对象-继承

# 目标

- 继承的概念
- 单继承
- 多继承
- 子类重写父类的同名属性和方法
- 子类调用父类的同名属性和方法
- 多层继承
- super()
- 私有属性和私有方法

# 一. 继承的概念

生活中的继承，一般指的是子女继承父辈的财产。

![](assets/oop_inherit/1.png)

- 拓展1：经典类或旧式类

不由任意内置类型派生出的类，称之为经典类。

```python
class 类名:
    代码
    ......
```

- 拓展2：新式类

```python
class 类名(object):
  代码
```



Python面向对象的继承指的是多个类之间的所属关系，即子类默认继承父类的所有属性和方法，具体如下：

``` python
# 父类A
class A(object):
    def __init__(self):
        self.num = 1

    def info_print(self):
        print(self.num)

# 子类B
class B(A):
    pass


result = B()
result.info_print()  # 1
```

> 在Python中，所有类默认继承object类，object类是顶级类或基类；其他子类叫做派生类。



# 二. 单继承

> 故事主线：一个煎饼果子老师傅，在煎饼果子界摸爬滚打多年，研发了一套精湛的摊煎饼果子的技术。师父要把这套技术传授给他的唯一的最得意的徒弟。

分析：徒弟是不是要继承师父的所有技术？

``` python
# 1. 师父类
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')

        
# 2. 徒弟类
class Prentice(Master):
    pass


# 3. 创建对象daqiu
daqiu = Prentice()
# 4. 对象访问实例属性
print(daqiu.kongfu)
# 5. 对象调用实例方法
daqiu.make_cake()
```



# 三. 多继承

> 故事推进：daqiu是个爱学习的好孩子，想学习更多的煎饼果子技术，于是，在百度搜索到黑马程序员，报班学习煎饼果子技术。

所谓多继承意思就是一个类同时继承了多个父类。

``` python
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


# 创建学校类
class School(object):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class Prentice(School, Master):
    pass


daqiu = Prentice()
print(daqiu.kongfu)
daqiu.make_cake()
```

> 注意：当一个类有多个父类的时候，默认使用第一个父类的同名属性和方法。



# 四. 子类重写父类同名方法和属性

> 故事：daqiu掌握了师父和培训的技术后，自己潜心钻研出自己的独门配方的一套全新的煎饼果子技术。

``` python
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class School(object):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


# 独创配方
class Prentice(School, Master):
    def __init__(self):
        self.kongfu = '[独创煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


daqiu = Prentice()
print(daqiu.kongfu)
daqiu.make_cake()

print(Prentice.__mro__)
```

> 子类和父类具有同名属性和方法，默认使用子类的同名属性和方法。



# 五. 子类调用父类的同名方法和属性

> 故事：很多顾客都希望也能吃到古法和黑马的技术的煎饼果子。

``` python
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class School(object):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class Prentice(School, Master):
    def __init__(self):
        self.kongfu = '[独创煎饼果子配方]'

    def make_cake(self):
        # 如果是先调用了父类的属性和方法，父类属性会覆盖子类属性，故在调用属性前，先调用自己子类的初始化
        self.__init__()
        print(f'运用{self.kongfu}制作煎饼果子')

    # 调用父类方法，但是为保证调用到的也是父类的属性，必须在调用方法前调用父类的初始化
    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)


daqiu = Prentice()

daqiu.make_cake()

daqiu.make_master_cake()

daqiu.make_school_cake()

daqiu.make_cake()
```



# 六. 多层继承

> 故事：N年后，daqiu老了，想要把所有技术传承给自己的徒弟。

``` python
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class School(object):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class Prentice(School, Master):
    def __init__(self):
        self.kongfu = '[独创煎饼果子配方]'

    def make_cake(self):
        self.__init__()
        print(f'运用{self.kongfu}制作煎饼果子')

    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)


# 徒孙类
class Tusun(Prentice):
    pass


xiaoqiu = Tusun()

xiaoqiu.make_cake()

xiaoqiu.make_school_cake()

xiaoqiu.make_master_cake()

```



# 七. super()调用父类方法

``` python
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

        # 方法2.1
        # super(School, self).__init__()
        # super(School, self).make_cake()

        # 方法2.2
        super().__init__()
        super().make_cake()


class Prentice(School):
    def __init__(self):
        self.kongfu = '[独创煎饼果子技术]'

    def make_cake(self):
        self.__init__()
        print(f'运用{self.kongfu}制作煎饼果子')

    # 子类调用父类的同名方法和属性：把父类的同名属性和方法再次封装
    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)

    # 一次性调用父类的同名属性和方法
    def make_old_cake(self):
        # 方法一：代码冗余；父类类名如果变化，这里代码需要频繁修改
        # Master.__init__(self)
        # Master.make_cake(self)
        # School.__init__(self)
        # School.make_cake(self)

        # 方法二: super()
        # 方法2.1 super(当前类名, self).函数()
        # super(Prentice, self).__init__()
        # super(Prentice, self).make_cake()

        # 方法2.2 super().函数()
        super().__init__()
        super().make_cake()


daqiu = Prentice()

daqiu.make_old_cake()
```

> 注意：使用super() 可以自动查找父类。调用顺序遵循 `__mro__` 类属性的顺序。比较适合单继承使用。



# 八. 私有权限

## 8.1 定义私有属性和方法

在Python中，可以为实例属性和方法设置私有权限，即设置某个实例属性或实例方法不继承给子类。

> 故事：daqiu把技术传承给徒弟的同时，不想把自己的钱(2000000个亿)继承给徒弟，这个时候就要为`钱`这个实例属性设置私有权限。

设置私有权限的方法：在属性名和方法名 前面 加上两个下划线 __。

``` python
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class School(object):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class Prentice(School, Master):
    def __init__(self):
        self.kongfu = '[独创煎饼果子配方]'
        # 定义私有属性
        self.__money = 2000000

    # 定义私有方法
    def __info_print(self):
        print(self.kongfu)
        print(self.__money)

    def make_cake(self):
        self.__init__()
        print(f'运用{self.kongfu}制作煎饼果子')

    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)


# 徒孙类
class Tusun(Prentice):
    pass


daqiu = Prentice()
# 对象不能访问私有属性和私有方法
# print(daqiu.__money)
# daqiu.__info_print()

xiaoqiu = Tusun()
# 子类无法继承父类的私有属性和私有方法
# print(xiaoqiu.__money)  # 无法访问实例属性__money
# xiaoqiu.__info_print()
```

> 注意：私有属性和私有方法只能在类里面访问和修改。

## 8.2 获取和修改私有属性值

在Python中，一般定义函数名`get_xx`用来获取私有属性，定义`set_xx`用来修改私有属性值。

``` python
class Master(object):
    def __init__(self):
        self.kongfu = '[古法煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class School(object):
    def __init__(self):
        self.kongfu = '[黑马煎饼果子配方]'

    def make_cake(self):
        print(f'运用{self.kongfu}制作煎饼果子')


class Prentice(School, Master):
    def __init__(self):
        self.kongfu = '[独创煎饼果子配方]'
        self.__money = 2000000

    # 获取私有属性
    def get_money(self):
        return self.__money

    # 修改私有属性
    def set_money(self):
        self.__money = 500

    def __info_print(self):
        print(self.kongfu)
        print(self.__money)

    def make_cake(self):
        self.__init__()
        print(f'运用{self.kongfu}制作煎饼果子')

    def make_master_cake(self):
        Master.__init__(self)
        Master.make_cake(self)

    def make_school_cake(self):
        School.__init__(self)
        School.make_cake(self)


# 徒孙类
class Tusun(Prentice):
    pass


daqiu = Prentice()

xiaoqiu = Tusun()
# 调用get_money函数获取私有属性money的值
print(xiaoqiu.get_money())
# 调用set_money函数修改私有属性money的值
xiaoqiu.set_money()
print(xiaoqiu.get_money())
```



# 九. 总结

- 继承的特点

  - 子类默认拥有父类的所有属性和方法
  - 子类重写父类同名方法和属性
  - 子类调用父类同名方法和属性

- super()方法快速调用父类方法

- 私有权限

  - 不能继承给子类的属性和方法需要添加私有权限
  - 语法

  ``` python
  class 类名():
    # 私有属性
    __属性名 = 值
  
    # 私有方法
    def __函数名(self):
      代码
  ```

  