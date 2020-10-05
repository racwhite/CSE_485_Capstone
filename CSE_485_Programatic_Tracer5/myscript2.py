def fun():
    print("got here")
    a = 3.56235
    b = 2.5
    c = a + b
    d = thing1()
    return "GFG"

def thing1():
    print("in thing1")
    a = 1+2
    return a
# global trace function is invoked here and
# local trace function is set for check()
def check():
    e = 5
    print("in check")
    fun()
    return fun()

check()
a = 2
a = 3.2
