#! /usr/bin/env python3


def fibonacci(i):
    if i <= 1:
        return i
    else:
        return fibonacci(i - 1) + fibonacci(i - 2)



print("The first 5 numbers in the fibonacci sequence are:")
for i in range(5):
    print(fibonacci(i))