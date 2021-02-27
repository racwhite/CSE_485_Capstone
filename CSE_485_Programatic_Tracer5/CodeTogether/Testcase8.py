#!/usr/bin/env python3

import myscript4
print("Test case 8")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
myscript4.step()
print(myscript4.thing1.CactusStack.print_tree())
myscript4.quit()
print("should be at line 1 --> a = 0")