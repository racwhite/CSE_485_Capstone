#!/usr/bin/env python3

import myscript4

# Test case 1
# Testing basic step function
print("Test case 1")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()

for i in range(15):
    myscript4.step()
myscript4.quit()
print("should be at linenumber 22 --> e = 5")