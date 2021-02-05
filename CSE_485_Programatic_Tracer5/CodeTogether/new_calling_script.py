import Tracer

# set filename

#Tracer.setfilename("/threads2.py")
Tracer.setfilename("/myscript2.py")


#example of breakpoints threaded threads2.py
# for i in range(1):
#     Tracer.commandinput('step', None)
# Tracer.commandinput('breakpoint', [31])
# Tracer.commandinput('step', None)
# Tracer.commandinput('breakpoint',[51])
# for i in range(5):
#     Tracer.commandinput('step', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

#example of 2 stepouts non-threaded myscript2.py

#Tracer.startrun()
# for i in range(15):
#     Tracer.commandinput('step', None)
# #Tracer.commandinput('stepout', None)
# #Tracer.commandinput('step', None)
# #Tracer.commandinput('stepout', None)
# #Tracer.commandinput('pause', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

#example of 2 stepouts non-threaded myscript2.py

# for i in range(15):
#     Tracer.commandinput('step', None)
# Tracer.commandinput('stepout', None)
# #Tracer.commandinput('step', None)
# #Tracer.commandinput('stepout', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

#example of stepover non-threaded myscript2.py

# for i in range(16):
#     Tracer.commandinput('step', None)
# Tracer.commandinput('stepover', None)
# #Tracer.commandinput('step', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

#example of stepover and breakpoint on function call non-threaded myscript2.py

# Tracer.commandinput('breakpoint', [7])
# Tracer.commandinput('stepover', None)
# #Tracer.commandinput('step', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

#example of stepover and breakpoint on function call non-threaded myscript2.py

# Tracer.commandinput('breakpoint', [7])
# Tracer.commandinput('stepover', None)
# Tracer.commandinput('step', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

#example of stepover and breakpoint not on function call non-threaded myscript2.py

# Tracer.commandinput('breakpoint', [6])
# Tracer.commandinput('stepover', None)
# #Tracer.commandinput('step', None)
# Tracer.commandinput('quit', None)
# Tracer.startrun()

# Test case 0

print("Test case 0")
#myscript4.analysis()

for i in range(15):
    Tracer.commandinput('step', None)
Tracer.commandinput("quit", None)
print(Tracer.command)
Tracer.startrun()

Tracer.setfilename("/helloworld.py")
for i in range(2):
    Tracer.commandinput('step', None)
Tracer.commandinput("quit", None)
Tracer.startrun()
print("should be at linenumber 4 in helloworld.py")


# Test case 1

# Testing basic step function
# print("Test case 1")
# myscript4.thing1.setFilePath("/myscript2.py")
# myscript4.start()

# for i in range(15):
#     myscript4.step()
# myscript4.quit()
# print("should be at linenumber 22 --> e = 5")

# Test case 2
# Testing stepover (as intended)

# print("Test case 2")
# myscript4.thing1.setFilePath("/myscript2.py")
# myscript4.start()
# ## TODO: Step x times to line 46
# for i in range(11):
#     myscript4.step()
# myscript4.stepover()
# myscript4.step()
# myscript4.quit()
# print("should be at linenumber 47 --> fun()")

# Test case 3
# Testing break, breakpoint implementation, and continue_run

# print("Test case 3")
# myscript4.thing1.setFilePath("/myscript2.py")
# myscript4.start()

# myscript4.addbreakpoint([22])
# myscript4.continue_run()
# myscript4.quit()
# print("should be at linenumber 22 --> e = 5")

# Test case 4
# Testing stepout from within a function

# print("Test case 4")
# myscript4.thing1.setFilePath("/myscript2.py")
# myscript4.start()
# # myscript4.analysis()
# for i in range(15):
#     myscript4.step()
# myscript4.stepout()
# myscript4.continue_run()
# myscript4.quit()
# print("should be at linenumber 50 --> fun() (or end of program)")
# print("Should be at the end of the program in myscript2.py")

# Test case 5
# Testing remove breakpoint

# print("Test case 5")
# myscript4.thing1.setFilePath("/myscript2.py")
# myscript4.start()
# # myscript4.analysis()
# myscript4.addbreakpoint([22, 24])
# myscript4.removebreakpoint(22)
# myscript4.continue_run()
# myscript4.quit()
# print("should be at linenumber 47 --> fun()")
# print("Should be at line 24 in myscript2.py")
