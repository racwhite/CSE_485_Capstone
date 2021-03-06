#!/usr/bin/env python3

import myscript5

"""multiple Programs"""

#tracer = myscript5.Python_tracer()
#tracer.setFilePath("/myscript2.py")
#tracer.start()
#for i in range(18):
#    tracer.step()
#tracer.stepover()
#tracer.step()
#tracer.stepout()
#print('quitting')
#tracer.quit()
#print('quitted')
#tracer.setFilePath("/myscript2.py")
#tracer.start()
#for i in range(18):
#    tracer.step()
#tracer.stepover()
#tracer.step()
#tracer.stepout()
#print('quitting')
#tracer.quit()
#print('quitted')

""" multiple programs with stepping """

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(1):
#     tracer.step()
# tracer.quit()
# tracer.setFilePath("/helloworld.py")
# tracer.start()
# for i in range(1):
#     tracer.step()
# tracer.quit()

"""Testing stepover not on function"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(20):
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
# tracer.quit()

'''100 steps in a row'''

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(100):
#     tracer.step()

"""test continueRun() and addbreakpoint() end at line 30"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.addbreakpoint([30])
# tracer.continueRun()
# tracer.step()
# tracer.step()

"""test continueRun() and addbreakpoint() end at line 1 ***"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.addbreakpoint([29, 45, 46, 1, 47, 50])
# tracer.removebreakpoint(29)
# tracer.removebreakpoint(1)
# tracer.continueRun()
# tracer.removebreakpoint(45)
# print(tracer.CactusStack.print_tree())
# tracer.continueRun()
# print(tracer.CactusStack.print_tree())
# tracer.continueRun()
# tracer.continueRun()
# print(tracer.CactusStack.print_tree())
# tracer.quit()
# print(tracer.CactusStack.print_tree())

"""start with stepout()"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.stepout()

"""start with continueRun()"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.continueRun()
# tracer.quit()
# tracer.CactusStack.print_all_scopes()
# print(tracer.CactusStack.print_tree())

"""start with stepover() and followed by stepping"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.stepover()
# tracer.stepover()
# for i in range(17):
#     tracer.step()
# tracer.stepover()

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(17):
#     tracer.step()
# tracer.stepover()

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(121):
#     tracer.step()
# tracer.quit()

"""run alot of time past program"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# for i in range(1000):
#     tracer.step()
# tracer.CactusStack.print_all_scopes()
# print(tracer.CactusStack.print_tree())
# tracer.quit()

"""start and quit unique arragements"""

# tracer = myscript5.Python_tracer()
# tracer.setFilePath("/myscript2.py")
# tracer.start()
# tracer.step()
# tracer.CactusStack.print_all_scopes()
# print(tracer.CactusStack.print_tree())
# tracer.quit()
# tracer.start()
# tracer.step()
# tracer.CactusStack.print_all_scopes()
# print(tracer.CactusStack.print_tree())
# tracer.quit()