print(dir('__builtins__'))
A = 'A'
print(A.isupper())

def func2():
    a = 2
    print(locals())
    def insideFunction():
        nonlocal a
        a = 3
        b=3
        print(locals())
    insideFunction()
    c = 4
    print(locals())

func2()
print(locals())