import vars
import os
import trace
import sys
import time
import linecache
import importlib
import threading
import ctypes
import multiprocessing
from typing import List

# https://docs.python.org/3/library/threading.html#semaphore-objects
# Initialize our semaphore to 0 (no commands yet

semaphore = threading.Semaphore(0)
semaphore2 = threading.Semaphore(0)

#threadlocal = threading.local()
current_line = 1
filething = ""
set2 = True
threadslsit = []
running = True

# Import the student's code file.
student_code = importlib.import_module("helloworld")

#https://github.com/python/cpython/blob/master/Lib/trace.py

class killableThread(threading.Thread): 
    def __init__(self, target): 
        #threading.Thread.__init__(self)
        super().__init__() 
        #self.name = name 
        self.running = True
              
    def run(self): 
  
        # target function of the thread class 
        while self.running == True: 
            run_student_code()
        print('ended') 
    
    def quit(self):
        self.running = False

    def get_id(self): 
  
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')

class Tracer(trace.Trace):

    # def __init__(self, count=1, trace=1, countfuncs=0, countcallers=0,
    #             ignoremods=(), ignoredirs=(), infile=None, outfile=None,
    #             timing=False):--
    #     super().__init__(self)
    #def __init__(self, count=False, trace=True, ignoredirs=[sys.prefix, sys.exec_prefix]):
        #super().__init__(count, trace, ignoredirs)
        # self.current_line = 1
        # self.breakpointlist = []
        # self.command = []
    def __init__(self, count, trace, ignoredirs):
        super(Tracer, self).__init__(count=False, trace=True, ignoredirs=[sys.prefix, sys.exec_prefix])
        self.current_line = 1
        self.why = 'line'
        self.current_frame = sys._getframe(0)
        self.returnframe = sys._getframe(0)
        self.set1 = True
        self.set2 = True
        self.filething = ''
        self.var = 0
        self.var_mutex = threading.Lock()
        self.var_event = threading.Event()
        self.var2 = 0
        self.var_mutex2 = multiprocessing.Lock()
        self.var_event2 = multiprocessing.Event()
        self.filenamevar = ""
        self.quit_value = 0
        self.startval = True

    def modname(self, path):
        """Return a plausible module name for the patch."""

        base = os.path.basename(path)
        filename, ext = os.path.splitext(base)
        return filename
    
    def localtrace_trace(self, frame, why, arg):
        # Only run a round if the semaphore has an open resource
        # (i.e. the user asked us to run a line)
        # Not worrying about thread safety, but probably should
       
        # self.WaitUntil(1)
        # self.Set(0)
        if self.quit_value == 1:
            raise SystemExit()
        semaphore.acquire()
        # record the file name and line number of every trace
        filename = frame.f_code.co_filename
        self.filething = frame.f_code.co_filename
        lineno = frame.f_lineno
        self.current_line = lineno
        self.why = why
        self.current_frame = frame
        function = frame.f_code.co_name
        if self.quit_value == 1:
            pass

        if self.start_time:
            print('%.2f' % (time.time() - self.start_time))
        print("%s (%d): %s %s %s" % (filename, lineno, linecache.getline(filename, lineno), why, function))
        tracer.Set(1)
        return self.localtrace

    def globaltrace_lt(self, frame, why, arg):
        """Handler for call events.
        If the code block being entered is to be ignored, returns `None',
        else returns self.localtrace.
        """
        #lineno = frame.f_lineno
        #self.current_line = lineno
        #self.current_frame = frame
        #self.why = why
        #setattr(Tracer, "current_line", lineno)

        if why == 'call':
            code = frame.f_code
            filename = frame.f_globals.get('__file__', None)
            if filename:
                # XXX _modname() doesn't work right for packages, so
                # the ignore support won't work right for packages
                modulename = self.modname(filename)
                if modulename is not None:
                    ignore_it = self.ignore.names(filename, modulename)
                    if not ignore_it:
                        if self.trace:
                            print((" --- modulename: %s, funcname: %s %s"
                                    % (modulename, code.co_name, 'call')))
                            self.why = why
                            self.current_frame = frame
                        return self.localtrace
            else:
                return None

    def WaitUntil(self, v):
        while True:
            self.var_mutex.acquire()
            if self.var == v:
                self.var_mutex.release()
                return # Done waiting
            self.var_mutex.release()
            self.var_event.wait(1) # Wait 1 sec

    def WaitUntil2(self, v):
        while True:
            self.var_mutex2.acquire()
            if self.var2 == v:
                self.var_mutex2.release()
                return # Done waiting
            self.var_mutex2.release()
            self.var_event2.wait(1) # Wait 1 sec

    """
    This function is for setting a certain lock state v. Has parameters of v (int).
    """
    def Set(self, v):
        self.var_mutex.acquire()
        self.var = v
        self.var_mutex.release()
        self.var_event.set() # In case someone is waiting
        self.var_event.clear()

    def Set2(self, v):
        self.var_mutex2.acquire()
        self.var2 = v
        self.var_mutex2.release()
        self.var_event2.set() # In case someone is waiting
        self.var_event2.clear()


def b():
    print('in b()')

def a():
    print('in a()')
    b()

tracer = Tracer(count=False, trace=True, ignoredirs=[sys.prefix, sys.exec_prefix])
#r = tracer.run('exec(open("module1.py").read())')
#exec(open("module1.py").read())


# Running this in another thread allows us to synchronously accept commands
# (i.e. method calls to step_over, etc).
def run_student_code():
    # Assuming they will have a main, improvement possible here.
    #tracer.runctx("student_code.main()")
    globals = {}
    with open(tracer.filenamevar, 'rb') as file:
            globals.update({
            "__name__": "__main__",
            })
            thing5 = compile(file.read(), tracer.filenamevar,'exec')
            tracer.run(thing5)

def thread1():
    #tracer.WaitUntil(0)
    run_student_code()


def step():
    # No special implementation for now.
    # Need to define communication with the thread to specify what command
    # to run, after the semaphore is released. Should be a list of commands in this
    # implementation, since semaphore can have more than 1 resource available.
    # Will probably want to change implementation to not allow this.
    # Could use different thread management techniques, or set semaphore to max 1
    # (BoundedSemaphore).
    #tracer.Set2(0)
    #tracer.var2 = 0
    print('step')
    # tracer.WaitUntil2(0)
    #semaphore.acquire()
    semaphore.release()
    tracer.WaitUntil(1)

    
    #semaphore.acquire()
    #semaphore2.release()
    # tracer.Set(1)
    # tracer.WaitUntil(0)

   #tracer.Set2(1)

    #tracer.Set2(1)
    print('step2')
    print('step3')
    # if tracer.startval == False:
    #     tracer.var_mutex2.release()
    # while tracer.var2 == 0 and tracer.startval == False:
    #     #print('step')
    #     pass
    # tracer.startval = False
    # if tracer.var2 == 1:
    #     tracer.var_mutex2.acquire()
    
    #tracer.var_mutex2.release()
    #tracer.WaitUntil2(1)
    #tracer.Set2(0)
    #tracer.Set(0)
    #tracer.WaitUntil(1)
    #semaphore.release()
    #pass

# def continuerun()
#     tracer.Set(0)

#returnframe = ''
output = []
command = ['step']
breakpointlist = []
# For simplicity, will input commands.
# In final version, user will call them programmatically.
# Need to implement communication so we know when the thread is done and don't keep running.
# Also need communication for the variable data structure, line number data, etc - won't just
# print it out in the final version.

def setfilename(filename):
    tracer.filenamevar = os.getcwd() + filename

def breakpointcall():
    if tracer.current_line not in breakpointlist and tracer.current_line != 50:
        #semaphore.release()
        step()
        #time.sleep(.003)
        print(tracer.current_line)

    else:
        command.remove(command[0])
        tracer.set2 = True

#arg is a list of points for the breakpoint command
def commandinput(newcommand, args):
    if newcommand == 'pause':
        command.append('pause')
    if newcommand == 'step':
        command.append('step')
    if newcommand == 'stepover':
        command.append('stepover')
    if newcommand == 'stepout':
        command.append('stepout')
    if newcommand == 'breakpoint':
        command.append('breakpoint')
        for arg in args:
            if arg not in breakpointlist:
                breakpointlist.append(arg)        
    if newcommand == 'quit':
        command.append('quit')

def thing11():
    tracer.Set(1)

def startrun():
    #t = multiprocessing.Process(target=thread1)
    t = threading.Thread(target=thread1)
    #t2 = threading.Thread(target=test)
    #t = killableThread(target=thread1)
    #t2 = killableThread(target=test)
    #t.daemon = True
    t.start()
    #t2.start()
    threadslsit.append(t)
    #vars.current_line = 1

# def test():
#     while tracer.quit_value != 1:
    while True:
        tracer.Set(0)
        #tracer.WaitUntil(1)
        #print("tracer.why = ", tracer.why)
        #command = input("Input a command (in, out, over, or quit): ")
        if command == []:
            print(1)
            break
        if command[0] == 'quit':
            # This is where we safely implement quit.
            #tracer.quit_value = 1
            #step()
            # thread_id = t.ident
            # res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
            # if res > 1: 
            #     ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            #     print('Exception raise failure')
            # step()
            command[0] = 'step'
            #tracer.Set(1)
            #command.append('pause')
            #tracer.quitthread()
            #t.raise_exception()
            #startrun()
            tracer.quit_value = 1
            #t.terminate()
            #step()
            #t.join()
            #t = threading.Thread(target=thread1)
            #step()
            #step()
            #tracer.Set(1)
            # command[0] = 'pause'
            # quit()
            #return
            #step()
            #tracer.quit_value = 1
            # tracer.Set(0)
            # tracer.WaitUntil(1)
            # tracer.WaitUntil(1)
            # time.sleep(1)
            #tracer.Set(1)
            break
        elif command[0] == 'stepover':
            if tracer.why == 'call':
                print('yes')
                step()
                if tracer.set2 == True:
                    #breakpointlist.append(tracer.current_frame.f_back.f_lineno)
                    breakpointlist.append(tracer.current_frame.f_back.f_lineno+1)
                    output.append(tracer.current_line)
                    #print(tracer.current_frame.f_back.f_lineno)
                    tracer.set2 = False
                breakpointcall()
                #command.remove(command[0])
            else:
                command.remove(command[0])
        elif command[0] == 'step':
            step()
            command.remove(command[0])
        elif command[0] == 'stepout':
            #time.sleep(.004)
            #print("linecache =,%s," % linecache.getline(tracer.filething, tracer.current_line))
            #print("tracer.filething, tracer.current_line = ", tracer.filething, tracer.current_line)
            #print("tracer.current_frame = ", tracer.current_frame.f_back.f_lineno)
            if tracer.set2 == True:
                #breakpointlist.append(tracer.current_frame.f_back.f_lineno)
                breakpointlist.append(tracer.current_frame.f_back.f_lineno+1)
                output.append(tracer.current_line)
                #print(tracer.current_frame.f_back.f_lineno)
                tracer.set2 = False
            breakpointcall()
            #tracer.set2 = True
            #step()
            #command.remove(command[0])
        elif command[0] == 'breakpoint':
            output.append(tracer.current_line)
            breakpointcall()
        elif command[0] == 'pause':
            thing = input('paused')
            command.remove(command[0])
        
        if command[0] != 'pause':
            pass
            #tracer.Set2(1)
        # semaphore2.acquire()
        # if command[0] == 'step':
        #     command.remove(command[0])
        #     semaphore2.release()

        #tracer.WaitUntil2(1)
        # else:
        #     break
        #     #step_over()

    # We can optionally use join to prevent execution from ending
    # This depends on use case, but forces the thread to continue until all code is run.
    # Optimally, we would have a cancel command that would internally kill the thread safely
    # (never forcefully kill threads).
    print(output)
    print(breakpointlist)
    #t.join()
