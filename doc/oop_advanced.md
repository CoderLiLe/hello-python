# 面向对象进阶

# 目标

- 面向对象三大特性
- 类属性和实例属性
- 类方法和静态方法

# 1. 面向对象三大特性

- 封装
  - 将属性和方法书写到类的里面的操作即为封装
  - 封装可以为属性和方法添加私有权限
- 继承
  - 子类默认继承父类的所有属性和方法
  - 子类可以重写父类属性和方法
- 多态
  - 传入不同的对象，产生不同的结果



# 2. 多态

## 2.1 了解多态

多态指的是一类事物有多种形态，（一个抽象类有多个子类，因而多态的概念依赖于继承）。

- 定义：多态是一种使用对象的方式，子类重写父类方法，调用不同子类对象的相同父类方法，可以产生不同的执行结果
- 好处：调用灵活，有了多态，更容易编写出通用的代码，做出通用的编程，以适应需求的不断变化！
- 实现步骤：
  - 定义父类，并提供公共方法
  - 定义子类，并重写父类方法
  - 传递子类对象给调用者，可以看到不同子类执行效果不同

## 2.2 体验多态

``` python
class Dog(object):
    def work(self):  # 父类提供统一的方法，哪怕是空方法
        print('指哪打哪...')


class ArmyDog(Dog):  # 继承Dog类
    def work(self):  # 子类重写父类同名方法
        print('追击敌人...')


class DrugDog(Dog):
    def work(self):
        print('追查毒品...')


class Person(object):
    def work_with_dog(self, dog):  # 传入不同的对象，执行不同的代码，即不同的work函数
        dog.work()


ad = ArmyDog()
dd = DrugDog()

daqiu = Person()
daqiu.work_with_dog(ad)
daqiu.work_with_dog(dd)
```



# 3. 类属性和实例属性

## 3.1 类属性

### 3.1.1 设置和访问类属性

- 类属性就是 **类对象** 所拥有的属性，它被 **该类的所有实例对象 所共有**。
- 类属性可以使用 **类对象** 或 **实例对象** 访问。

``` python
class Dog(object):
    tooth = 10


wangcai = Dog()
xiaohei = Dog()

print(Dog.tooth)  # 10
print(wangcai.tooth)  # 10
print(xiaohei.tooth)  # 10
```

> 类属性的优点
>
> - **记录的某项数据 始终保持一致时**，则定义类属性。
> - **实例属性** 要求 **每个对象** 为其 **单独开辟一份内存空间** 来记录数据，而 **类属性** 为全类所共有 ，**仅占用一份内存**，**更加节省内存空间**。



### 3.1.2 修改类属性

类属性只能通过类对象修改，不能通过实例对象修改，如果通过实例对象修改类属性，表示的是创建了一个实例属性。

``` python
class Dog(object):
    tooth = 10


wangcai = Dog()
xiaohei = Dog()

# 修改类属性
Dog.tooth = 12
print(Dog.tooth)  # 12
print(wangcai.tooth)  # 12
print(xiaohei.tooth)  # 12

# 不能通过对象修改属性，如果这样操作，实则是创建了一个实例属性
wangcai.tooth = 20
print(Dog.tooth)  # 12
print(wangcai.tooth)  # 20
print(xiaohei.tooth)  # 12
```



## 3.2 实例属性

``` python
class Dog(object):
    def __init__(self):
        self.age = 5

    def info_print(self):
        print(self.age)


wangcai = Dog()
print(wangcai.age)  # 5
# print(Dog.age)  # 报错：实例属性不能通过类访问
wangcai.info_print()  # 5
```



# 4. 类方法和静态方法

## 4.1 类方法

### 4.1.1 类方法特点

- 需要用装饰器`@classmethod`来标识其为类方法，对于类方法，**第一个参数必须是类对象**，一般以`cls`作为第一个参数。



### 4.1.2 类方法使用场景

- 当方法中 **需要使用类对象** (如访问私有类属性等)时，定义类方法
- 类方法一般和类属性配合使用

``` python
class Dog(object):
    __tooth = 10

    @classmethod
    def get_tooth(cls):
        return cls.__tooth


wangcai = Dog()
result = wangcai.get_tooth()
print(result)  # 10
```



## 4.2 静态方法

### 4.2.1 静态方法特点

- 需要通过装饰器`@staticmethod`来进行修饰，**静态方法既不需要传递类对象也不需要传递实例对象（形参没有self/cls）**。
- 静态方法 也能够通过 **实例对象** 和 **类对象** 去访问。

### 4.2.2 静态方法使用场景

- 当方法中 **既不需要使用实例对象**(如实例对象，实例属性)，**也不需要使用类对象** (如类属性、类方法、创建实例等)时，定义静态方法
- **取消不需要的参数传递**，有利于 **减少不必要的内存占用和性能消耗**

``` python
class Dog(object):
    @staticmethod
    def info_print():
        print('这是一个狗类，用于创建狗实例....')


wangcai = Dog()
# 静态方法既可以使用对象访问又可以使用类访问
wangcai.info_print()
Dog.info_print()
```

## 5. 可见性和属性装饰器

在很多面向对象编程语言中，对象的属性通常会被设置为私有（private）或受保护（protected）的成员，简单的说就是不允许直接访问这些属性；对象的方法通常都是公开的（public），因为公开的方法是对象能够接受的消息，也是对象暴露给外界的调用接口，这就是所谓的访问可见性。在 Python 中，可以通过给对象属性名添加前缀下划线的方式来说明属性的访问可见性，例如，可以用`__name`表示一个私有属性，`_name`表示一个受保护属性，代码如下所示。

```python
class Student:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def study(self, course_name):
        print(f'{self.__name}正在学习{course_name}.')


stu = Student('王大锤', 20)
stu.study('Python程序设计')
print(stu.__name)  # AttributeError: 'Student' object has no attribute '__name'
```

上面代码的最后一行会引发`AttributeError`（属性错误）异常，异常消息为：`'Student' object has no attribute '__name'`。由此可见，以`__`开头的属性`__name`相当于是私有的，在类的外面无法直接访问，但是类里面的`study`方法中可以通过`self.__name`访问该属性。需要说明的是，大多数使用 Python 语言的人在定义类时，通常不会选择让对象的属性私有或受保护，正如有一句名言说的：“**We are all consenting adults here**”（大家都是成年人），成年人可以为自己的行为负责，而不需要通过 Python 语言本身来限制访问可见性。事实上，大多数的程序员都认为**开放比封闭要好**，把对象的属性私有化并非必不可少的东西，所以 Python 语言并没有从语义上做出最严格的限定，也就是说上面的代码如果你愿意，用`stu._Student__name`的方式仍然可以访问到私有属性`__name`，有兴趣的读者可以自己试一试。

## 6. 动态属性

Python 语言属于动态语言，维基百科对动态语言的解释是：“在运行时可以改变其结构的语言，例如新的函数、对象、甚至代码可以被引进，已有的函数可以被删除或是其他结构上的变化”。动态语言非常灵活，目前流行的 Python 和 JavaScript 都是动态语言，除此之外，诸如 PHP、Ruby 等也都属于动态语言，而 C、C++ 等语言则不属于动态语言。

在 Python 中，我们可以动态为对象添加属性，这是 Python 作为动态类型语言的一项特权，代码如下所示。需要提醒大家的是，对象的方法其实本质上也是对象的属性，如果给对象发送一个无法接收的消息，引发的异常仍然是`AttributeError`。

```python
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student('王大锤', 20)
stu.sex = '男'  # 给学生对象动态添加sex属性
```

如果不希望在使用对象时动态的为对象添加属性，可以使用 Python 语言中的`__slots__`魔法。对于`Student`类来说，可以在类中指定`__slots__ = ('name', 'age')`，这样`Student`类的对象只能有`name`和`age`属性，如果想动态添加其他属性将会引发异常，代码如下所示。

```python
class Student:
    __slots__ = ('name', 'age')

    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student('王大锤', 20)
# AttributeError: 'Student' object has no attribute 'sex'
stu.sex = '男'
```


# 7. 总结

- 面向对象三大特性
  - 封装
  - 继承
  - 多态
- 类属性
  - 归属于类对象的属性，所有对象共有的属性
- 实例属性
- 类方法

``` python
@classmethod
def xx():
  代码
```

- 静态方法

``` python
@staticmethod
def xx():
  代码
```

Python 是动态类型语言，Python 中的对象可以动态的添加属性，对象的方法其实也是属性，只不过和该属性对应的是一个可以调用的函数。在面向对象的世界中，**一切皆为对象**，我们定义的类也是对象，所以**类也可以接收消息**，对应的方法是类方法或静态方法。通过继承，我们**可以从已有的类创建新类**，实现对已有类代码的复用。