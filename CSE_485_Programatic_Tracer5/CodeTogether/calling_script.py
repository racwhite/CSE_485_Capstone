#!/usr/bin/env python3

import myscript4

"""
Test case 0 
15 steps into myscript2.py and then quit and change programs to helloworld.py and step 2 times
"""
print("Test case 0")

myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
#myscript4.analysis()

for i in range(15):
    myscript4.step()
myscript4.quit()

myscript4.thing1.setFilePath("/helloworld.py")
myscript4.start()
for i in range(2):
    myscript4.step()
myscript4.quit()

print("should be at linenumber 4 in helloworld.py")


# Test case 1
# Testing basic step function
print("Test case 1")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()

for i in range(15):
    myscript4.step()
myscript4.quit()
print("should be at linenumber 22 --> e = 5")

# Test case 2 (has issues)
# Testing stepover (as intended)
print("Test case 2")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
## TODO: Step x times to line 46
for i in range(13):
    myscript4.step()
myscript4.stepover()
myscript4.step()
myscript4.quit()
print("should be at linenumber 47 --> fun()")

# Test case 3
# Testing break, breakpoint implementation, and continue_run
print("Test case 3")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()

myscript4.addbreakpoint([22])
myscript4.continue_run()
myscript4.quit()
print("should be at linenumber 22 --> e = 5")

# Test case 4
# Testing stepout from within a function
print("Test case 4")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
# myscript4.analysis()
for i in range(15):
    myscript4.step()
myscript4.stepout()
myscript4.continue_run()
myscript4.quit()
print("should be at linenumber 50 --> fun() (or end of program)")
print("Should be at the end of the program in myscript2.py")

# Test case 5
# Testing remove breakpoint
print("Test case 5")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
# myscript4.analysis()
myscript4.addbreakpoint([22, 24])
myscript4.removebreakpoint(22)
myscript4.continue_run()
myscript4.quit()
print("should be at linenumber 47 --> fun()")
print("Should be at line 24 in myscript2.py")
