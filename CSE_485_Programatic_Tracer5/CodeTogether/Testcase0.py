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