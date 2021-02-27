#!/usr/bin/env python3

import myscript4

# Test case 5
# Testing remove breakpoint
print("Test case 5")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
myscript4.step()
# myscript4.analysis()
myscript4.addbreakpoint([22, 24])
myscript4.removebreakpoint(22)
myscript4.continue_run()
print(myscript4.thing1.CactusStack.print_tree())
myscript4.quit()
print("should be at linenumber 25 --> t = 12 ")
print("Should be at line 25 in myscript2.py")