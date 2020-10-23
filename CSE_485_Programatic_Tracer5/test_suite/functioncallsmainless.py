#! /usr/bin/env python3


def math(number):
    b = 4
    return number + b


def math2(i):
    a = 10 + i
    c = math_helper(a)
    d = 40
    return c + d


def math_helper(a):
    xyz = 'str'
    return a + 10


b = 6
b = math(b)
a = math2(2)
print(b)
print(a)
