#!/usr/bin/env python3

import myscript5

"""multiple Programs"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(18):
#     tracer.step()
# tracer.stepover()
# tracer.step()
# tracer.stepout()
# print('quitting')
# tracer.quit()
# print('quitted')
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(18):
#     tracer.step()
# tracer.stepover()
# tracer.step()
# tracer.stepout()
# print('quitting')
# tracer.quit()
# print('quitted')

"""Testing stepover not on function"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(19):
#     tracer.step()
# tracer.stepover()
# tracer.quit()

"""Testing double step over in a row on top of functions"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(18):
#     tracer.step()
# tracer.stepover()
# tracer.stepover()
# tracer.quit()

"""stepover on inner function for_loop() inside function check()"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(21):
#     tracer.step()
# tracer.stepover()

"""stepout on inner function for_loop() in check()"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(22):
#     tracer.step()
# tracer.stepout()

"""stepout in check() and fun()"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(22):
#     tracer.step()
# tracer.stepout()
# for i in range(4):
#      tracer.step()
# tracer.stepout()
# tracer.step()
# tracer.step()
# tracer.step()
# tracer.stepout()
# tracer.step()
# tracer.step()
# tracer.stepout()
# tracer.step()
# tracer.step()
# tracer.stepout()
# tracer.step()
# tracer.step()
# tracer.step()
# tracer.stepout()


"""stepout on inner function check()"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(19):
#     tracer.step()
# tracer.stepout()
# tracer.step()

'''stepout in module'''

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(18):
#     tracer.step()
# tracer.stepout()

'''stepover at begining of the program'''

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.stepover()
# tracer.step()

'''two steps at the begining'''

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.step()
# tracer.step()

'''a bunch of steps in a row'''

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(100):
#     tracer.step()

tracer = myscript5.Python_tracer()
tracer.setFilePath("/myscript2.py")
tracer.start()
tracer.addbreakpoint([30])
tracer.continueRun()
tracer.step()
tracer.step()