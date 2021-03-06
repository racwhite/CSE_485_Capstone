from cactus import Node
import LinkedList
import analysis3
import importlib.util
from sys import settrace
import sys
import linecache
import os
import io
import inspect
import threading

class Python_tracer():

    def __init__(self):
        self.filepath = ''
        self.lastlineofprogram = 0
        self.commandQueue = []
        self.threads = None
        self.var = 0
        self.var_mutex = threading.Lock()
        self.var_event = threading.Event()
        self.command = 'step'
        self.initialRun = 0
        self.breakpointlist = []
        self.curFrame = None
        self.curEvent = ''
        self.quitValue = 0
        self.CactusStack = None
        self.scope = None

    def reset(self):
        #self.lastlineofprogram = 0
        self.commandQueue = []
        self.threads = None
        self.var = 0
        self.var_mutex = threading.Lock()
        self.var_event = threading.Event()
        self.command = 'step'
        self.initialRun = 0
        self.breakpointlist = []
        self.curFrame = None
        self.quitValue = 0
        self.CactusStack = None
        self.scope = None

    def setFilePath(self, filepathParam):
        self.filepath = filepathParam
        self.lastlineofprogram = self.getlastline(self.filepath[1:])
    
    def getlastline(self, filepath):
        ProgramlineNumberCounter = 0
        with open(filepath, 'r') as file:
            for line in file:
                ProgramlineNumberCounter = ProgramlineNumberCounter + 1
        print("In getlastline. Last line of file is line # " + str(ProgramlineNumberCounter))
        return ProgramlineNumberCounter
    
    def injectTracer(self):
        globals = {}
        # globals.update({
        #     "__name__": "__main__",
        # })
        currentDirectorypath = os.getcwd()+self.filepath
        with open(currentDirectorypath, 'rb') as file:
            codeObject = compile(file.read(), currentDirectorypath, 'exec')
            settrace(self.mainTracer)
            exec(codeObject, globals, None)

    def mainTracer(self, frame, event, arg):
        self.curFrame = frame
        self.curEvent = event
        # if self.scope is None or self.scope.is_empty():
        #     self.scope = LinkedList.FrameList()
        #     self.scope.insert_frame(frame.f_code.co_name, frame.f_locals)
        #     del self.scope.current_frame.frame_vars['__builtins__']
        #     self.scope.insert_frame(frame.f_code.co_name, frame.f_locals)
        # else:
        #     if event == 'call'or event == 'line':
        #         self.scope.insert_frame(frame.f_code.co_name, frame.f_locals)
        #     if event == 'return':
        #         self.scope.exit_frame()
        if self.CactusStack is None or self.CactusStack.is_empty():
            self.CactusStack = Node(frame.f_code.co_name, frame.f_locals)
            del self.CactusStack.current_frame.vars['__builtins__']
        else:
            self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
        print('waiting at mainTracer')
        if self.initialRun != 0:
            self.WaitUntil(1)
        if self.quitValue == 1:
            self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
            raise SystemExit()
        if self.command != "stepover" and self.command != 'stepout':
            self.Set(0)
        if self.command == "stepover" and frame.f_code.co_name == '<module>':
            print('here I got')
            self.Set(0)
        print('mainTracer')
        #if self.initialRun != 0:
        print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno))
        if event == 'call' and self.command == 'step':
            return self.innerFunction
        if event == 'call' and self.command == 'stepover' and frame.f_code.co_name != '<module>':
            return self.innerFunctionStepover
        if self.command == 'stepout':
            return self.innerFunctionStepout
        if self.command == "stepover" or self.command == "stepout":
            self.Set(0)
        #return self.mainTracer

    def innerFunction(self, frame, event, arg):
        self.curFrame = frame
        self.curEvent = event
        self.WaitUntil(1)
        self.Set(0)
        if self.quitValue == 1:
            #self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
            raise SystemExit()
        if event == 'return':
            self.CactusStack.pop()
        # if event == 'return':
        #     self.scope.exit_frame()
        # self.scope.insert_frame(frame.f_code.co_name, frame.f_locals)
        # if event == 'return':
        #     self.scope.insert_frame(frame.f_code.co_name, frame.f_locals)
        #     self.scope.exit_frame()
        print('inner function')
        if self.initialRun != 0:
            print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno))
        if self.initialRun == 0:
            self.initialRun += 1
        # if self.quitValue == 1:
        #     self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals)) 
        #     raise SystemExit()

    def innerFunctionStepover(self, frame, event, arg):
        self.curFrame = frame
        self.curEvent = event
        print('inner function stepover')
        #print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno))

    def innerFunctionStepout(self, frame, event, arg):
        self.curFrame = frame
        self.curEvent = event
        print('inner function stepout')
        # if event == 'return':
        #     self.Set(0)

    # def stepoutFucntion(self, frame, event, arg):
    #     self.WaitUntil(1)
    #     self.Set(0)  

    def TracerThread(self):
        self.injectTracer()

    def start(self):
        self.reset()
        t1 = threading.Thread(name='TracerThread', target=self.TracerThread)
        t1.start()
        self.threads = t1
        #self.step()

    def quitEndProgram(self):
        settrace(None)
        self.quitValue = 1
        self.Set(1)

    def quit(self):
        settrace(None)
        self.quitValue = 1
        self.Set(1)
        #self.scope.print_all_frames()
        try:
            self.threads.join()
            self.CactusStack.reset_scopes()
            self.reset()
        except:
            print("Error: Used quit without a coresponding start. please use start to start tracing.")

    def Set(self, v):
        self.var_mutex.acquire()
        self.var = v
        self.var_mutex.release()
        self.var_event.set() # In case someone is waiting
        self.var_event.clear()

    def WaitUntil(self, v):
        while True:
            self.var_mutex.acquire()
            if self.var == v:
                self.var_mutex.release()
                return # Done waiting
            self.var_mutex.release()
            self.var_event.wait(1) # Wait 1 sec

    def commandHandler(self, command):
        if self.curFrame is not None and (int(self.lastlineofprogram) == int(self.curFrame.f_lineno)):
            #print("reached last line of file")
            self.quit()
        else:
            self.command = command
            self.Set(1)
            self.WaitUntil(0)

    def step(self):
        newCommand = "step"
        self.commandHandler(newCommand)

    def stepover(self):
        if self.curEvent == 'call':
            newCommand = "stepover"
            self.commandHandler(newCommand)
        else:
            print('can not stepover because not over function')

    def stepout(self):
        returnFrame = self.curFrame.f_code.co_name
        callNum = 1
        while(True):
            if callNum == 0:
                print("inner break")
                break
            else:
                if self.curEvent == 'call' and self.curFrame.f_code.co_name == returnFrame:
                    callNum = callNum + 1
                if self.curEvent == 'return' and self.curFrame.f_code.co_name == returnFrame:
                    callNum = callNum - 1
                print("callNum = ", callNum)
                newCommand = 'step'
                self.commandHandler(newCommand)

    def continueRun(self):
        if self.curFrame == None:
            self.step()
        # if self.curFrame.f_lineno == 1:
        #     self.step()
            #print(linecache.getline(self.curFrame.f_code.co_name, self.curFrame.f_lineno))
        while self.curFrame.f_lineno not in self.breakpointlist and self.curFrame.f_lineno != self.lastlineofprogram:
            self.commandHandler('step')
        self.step()

    def addbreakpoint(self, breakpointNew):
        for breakpointElement in breakpointNew:
            self.breakpointlist.append(breakpointElement)

    def removebreakpoint(self, breakpointToRemove):
        self.breakpointlist.remove(breakpointToRemove)
    
