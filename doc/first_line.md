# print

```python
# 输出数字
print(520)
print(98.5)

# 输出字符串
print('hello world') # 单引号内内容直接输出
print("hello world") # 双引号内内容直接输出

# 输出计算后内容 
print(3 + 1) # 含有运算符的表达式，会计算

# 输出数据到文件当中
fp = open('D:/test.txt', 'a+') # 输出在文件中，a+表示以读写功能创建，文件不存在就创建，存在的话就在文件内容后继续追加
print('hello world', file=fp)  # # A.所指定的盘符必须存在 B.使用file=fp 把打印内容输出到fp当中，不用file的话文件里没有东西
fp.close() 

# 不进行换行输出（输出内容在一行当中） 用逗号进行分隔
print('hello', 'world', 'Python')
```

> **注意**：上面代码中的圆括号、单引号都是在英文输入法状态下输入的，如果不小心写成了中文的圆括号或单引号，运行代码时会出现`SyntaxError: invalid character '（' (U+FF08)`或`SyntaxError: invalid character '‘' (U+2018)`这样的错误提示。

上面的代码只用到了一个名为`print`的函数，它可以帮助我们输出指定的内容；`print`函数圆括号中的`'hello, world'`是一个字符串，它代表了一段文本内容；在 Python 语言中，我们可以用单引号或双引号来表示一个字符串。不同于 C、C++ 或 Java 这样的编程语言，Python 代码中的语句不需要用分号来表示结束，也就是说，如果我们想再写一条语句，只需要回车换行即可，代码如下所示。此外，Python 代码也不需要通过编写名为`main`的入口函数来使其运行，提供入口函数是编写可执行的 C、C++ 或 Java 代码必须要做的事情，这一点很多程序员都不陌生，但是在 Python 语言中它并不是必要的。

> 提醒大家的是，写 Python 代码时，最好每一行只写一条语句。虽然，我们可以使用`;`作为分隔将多个语句写在一行中，但是这样做会让代码变得非常难看，不再具备良好的可读性。

## 注释

注释是编程语言的一个重要组成部分，用于在代码中解释代码的作用，从而达到增强代码可读性的目标。当然，我们也可以将代码中暂时不需要运行的代码段通过添加注释来去掉，这样当你需要重新使用这些代码的时候，去掉注释符号就可以了。简单的说，**注释会让代码更容易看懂但不会影响代码的执行结果**。

Python 中有两种形式的注释：

1. 单行注释：以`#`和空格开头，可以注释掉从`#`开始后面一整行的内容。
2. 多行注释：三个引号（通常用双引号）开头，三个引号结尾，通常用于添加多行说明性内容。

```python
"""
第一个Python程序 - hello, world

Version: 1.0
Author: CoderLiLe
"""
# print('hello, world')
print("你好，世界！")
```

## 转义字符
```python
# 转义字符
print('hello\nworld') # \+转义功能的首字符   n--newline的首字符表示换行

print('hello\tworld') # \t用了三个位置

print('helloooo\tworld') # \t用了四个位置

print('hello\rworld') # return  回车 只剩下world将hello进行了覆盖

print('hello\bworld') # back 退格 少一个o

print('http:\\\\www.baidu.com')  # \\打印出来是一个\

print('老师说：\‘大家好\’') # \是转义字符

print(r'hello\n world') # 原字符，不希望字符串中的转义字符起作用，就使用原字符，就是在字符串之前加上r或R

#print(r'hello\n world\') # 最后一个字符不能是反斜线\
print(r'hello\n world\\') # 最后一个字符可以是两个\\
```

## 二进制与字符编码

```python
print(chr(0b100111001011000))  # 0b表示为十六进制

print(ord('乘'))  # 十进制为20056
```
结果如下：

	乘
	20056
