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

    def reset(self):
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
        self.quitValue = 0

    def setFilePath(self, filepathParam):
        self.filepath = filepathParam
        self.lastlineofprogram = self.getlastline(self.filepath[1:])
    
    def getlastline(self, filepath):
        ProgramlineNumberCounter = 0
        with open(filepath, 'r') as file:
            for i in file:
                ProgramlineNumberCounter = ProgramlineNumberCounter + 1
        return ProgramlineNumberCounter
    
    def injectTracer(self):
        globals = {}
        globals.update({
            "__name__": "__main__",
        })
        currentDirectorypath = os.getcwd()+self.filepath
        with open(currentDirectorypath, 'rb') as file:
            codeObject = compile(file.read(), currentDirectorypath, 'exec')
            settrace(self.mainTracer)
            exec(codeObject, globals, None)

    def mainTracer(self, frame, event, arg):
        self.curFrame = frame
        self.curEvent = event
        print('waiting at mainTraer')
        if self.initialRun != 0:
            self.WaitUntil(1)
        if self.quitValue == 1:
            raise SystemExit()
        if self.command != "stepover" and self.command != 'stepout':
            self.Set(0)
        if self.initialRun == 0:
            print(str(frame.f_lineno) + '\t' + frame.f_code.co_name)
            self.initialRun = 1
        if self.command == "stepover" and frame.f_code.co_name == '<module>':
            print('here I got')
            self.Set(0)
        print('mainTracer')
        if self.initialRun != 0:
            print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno))
        if event == 'call' and self.command == 'step':
            return self.innerFunction
        if event == 'call' and self.command == 'stepover' and frame.f_code.co_name != '<module>':
            return self.innerFunctionStepover
        if self.command == 'stepout':
            return self.innerFunctionStepout
        if self.command == "stepover" or self.command == "stepout":
            self.Set(0)
        return self.mainTracer

    def innerFunction(self, frame, event, arg):
        self.curFrame = frame
        self.curEvent = event
        self.WaitUntil(1)
        if self.quitValue == 1:
            raise SystemExit()
        self.Set(0)
        print('inner function')
        print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno))

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
        self.step()

    def quit(self):
        settrace(None)
        self.quitValue = 1
        self.Set(1)
        try:
            self.threads.join()
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
        if self.curFrame.f_lineno == 1:
            self.step()
            #print(linecache.getline(self.curFrame.f_code.co_name, self.curFrame.f_lineno))
        while self.curFrame.f_lineno not in self.breakpointlist and self.curFrame.f_lineno != self.lastlineofprogram:
            self.commandHandler('step') 
    
    def addbreakpoint(self, breakpointNew):
        for breakpointElement in breakpointNew:
            self.breakpointlist.append(breakpointElement)

    def removebreakpoint(self, breakpointToRemove):
        self.breakpointlist.remove(breakpointToRemove)
    
