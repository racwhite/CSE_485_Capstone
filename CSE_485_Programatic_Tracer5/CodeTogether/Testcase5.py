#!/usr/bin/env python3

import myscript4

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