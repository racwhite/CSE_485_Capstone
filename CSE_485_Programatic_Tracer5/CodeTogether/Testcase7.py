#!/usr/bin/env python3

import myscript4
print("Test case 7")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
myscript4.step()
myscript4.addbreakpoint([23])
#myscript4.continue_run()
#myscript4.step()
myscript4.stepover()
myscript4.continue_run()
myscript4.stepover()
print(myscript4.thing1.CactusStack.print_tree())
myscript4.quit()
print("should be at line 24 --> t = 12")

