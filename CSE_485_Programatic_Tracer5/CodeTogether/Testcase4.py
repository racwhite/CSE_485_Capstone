#!/usr/bin/env python3

import myscript4
# Test case 4
# Testing stepout from within a function
print("Test case 4")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
# myscript4.analysis()
for i in range(17):
    myscript4.step()
myscript4.stepout()
#myscript4.step()
myscript4.continue_run()
print(myscript4.thing1.CactusStack.print_tree())
myscript4.quit()
print("should be at linenumber 50 --> a = 3.5 (or end of program)")
print("Should be at the end of the program in myscript2.py")