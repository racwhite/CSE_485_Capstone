#!/usr/bin/env python3

import myscript4

# Test case 2 (has issues)
# Testing stepover (as intended)
print("Test case 2")
myscript4.thing1.setFilePath("/myscript2.py")
myscript4.start()
## TODO: Step 16 times to line 46
for i in range(15):
    myscript4.step()
myscript4.stepover()
#myscript4.step()
myscript4.stepover()
#myscript4.step()
myscript4.quit()
print("should be at linenumber 47 --> fun()")