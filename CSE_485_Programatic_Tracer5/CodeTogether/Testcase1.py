#!/usr/bin/env python3

import sys
import myscript4

# Test case 1
# Testing basic step function
print("Test case 1")
myscript4.thing1.setFilePath("/myscript2.py")
#myscript4.thing1.setFilePath("/test/linkedlistmainless.py")
myscript4.start()

for i in range(101):
    myscript4.step()
print(myscript4.thing1.CactusStack.print_tree())
#myscript4.thing1.scope.print_all_frames()
myscript4.quit()
print("should be at linenumber 22 --> e = 5")