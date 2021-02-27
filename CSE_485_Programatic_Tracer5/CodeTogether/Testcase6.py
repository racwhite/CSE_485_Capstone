#!/usr/bin/env python3

import myscript4
print("Test case 6")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
myscript4.addbreakpoint([1, 30])
myscript4.continue_run()
myscript4.continue_run()
for i in range(7):
    myscript4.step()
myscript4.stepover()
myscript4.stepout()
# # why we need step here in between stepouts
myscript4.step()
myscript4.stepout()
myscript4.removebreakpoint(30)
myscript4.addbreakpoint([49, 50])
myscript4.continue_run()
myscript4.continue_run()
print(myscript4.thing1.CactusStack.print_tree())
myscript4.quit()