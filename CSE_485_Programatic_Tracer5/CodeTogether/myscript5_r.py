from cactus import Node
# import LinkedList
# import analysis3
import hoare_logic
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
        self.stepover_active = False
        self.stepover_call_depth = 0
        self.logic_checker = None

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
        self.logic_checker = None

    def setFilePath(self, filepathParam):
        self.filepath = filepathParam
        self.lastlineofprogram = self.getlastline(self.filepath[1:])
    
    def getlastline(self, filepath):
        programLineNumberCounter = 0
        with open(filepath, 'r') as file:
            for line in file:
                programLineNumberCounter += 1
        print("In getlastline. Last line of file is line # " + str(programLineNumberCounter))
        return programLineNumberCounter
    
    def injectTracer(self):
        globals = {}
        # globals.update({
        #     "__name__": "__main__",
        # })
        currentDirectorypath = os.getcwd()+self.filepath
        with open(currentDirectorypath, 'rb') as file:
            codeObject = compile(file.read(), currentDirectorypath, 'exec')
            settrace(self.mainTracer)
            #try:
            exec(codeObject, globals, None)
            print("exec() returned")
            #except:
            #    pass

    def mainTracer(self, frame, event, arg):
        '''
        This is a settrace() callback function.  It is the global callback
        function set during initialization.

        :param frame: frame object
        :param event String: "call", "line", "return", "exception", "opcode"
        :param arg:
        :return:    settrace() local callback function

        This function only processes the 'call' event.  During processing
        of the call event, the function sets the local callback function
        which will trace the lines within the called function.  Thus,
        innerFunction() and InnerFunctionStepover() trace line and return
        events.

        The first invocation is a call event to <module>
        '''     
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

        # push current frame onto CactusStack
        print("mainTracer(): push node ", frame.f_code.co_name)
        # if first time through
        if self.logic_checker is None:
            self.logic_checker = hoare_logic.program_conditions("conditions.txt")
        if self.CactusStack is None or self.CactusStack.is_empty():
            self.CactusStack = None
            self.scope = None
            self.CactusStack = Node(frame.f_code.co_name, frame.f_locals)
            self.CactusStack.reset_scopes()
            del self.CactusStack.current_frame.vars['__builtins__']
        else:
            # add node for current frame
            self.logic_checker.check_conditions({}, scopes=self.CactusStack.current_frame.vars)
            self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))


        print('waiting at mainTracer(): ', event, ' ', frame.f_code.co_name)
        # print the current source line
        print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno), end='')
        # wait for a commend
        self.WaitUntil(1)
        print('mainTracer(): ', self.command)

        # The normal means of quitting is when a local trace function
        # encounters a returm from <module>.
        # if commanded to quit, push frame and exit
        if self.quitValue == 1:
            print("mainTracer(): quitValue")
            self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
            self.logic_checker.check_conditions({}, scopes=self.CactusStack.current_frame.vars)
            raise SystemExit()
        if self.command != "stepover":
            self.Set(0)
        # one way that stepover must end, at outer scope                                                
        if self.command == "stepover" and frame.f_code.co_name == '<module>':
            print('here I got')
            self.Set(0)
        if event == 'call' and self.command == 'step':
            # set local settrace() callback function for stepping
            return self.innerFunction
        if event == 'call' and self.command == 'stepover' and frame.f_code.co_name != '<module>':
            self.stepover_call_depth += 1
            # switch settrace() local callback function to innerFunctionStepover()                                                                                                        
            return self.innerFunctionStepover

    def innerFunction(self, frame, event, arg):
        '''
        This is a settrace() local callback function.  This callback persists
        for the duration of the current frame; that is, for the current function.
        After processing a return event, the global callback again becomes
        active.

        :param frame: frame object
        :param event String: "line", "return", "exception", "opcode"
        :param arg:
        :return:    settrace() local callback function
        '''
        self.curFrame = frame
        self.curEvent = event
        print('waiting innerFunction(): ', event, frame.f_code.co_name)
        #if event == 'return':
        #    if 'return ' not in linecache.getline(self.filepath[1:], frame.f_lineno):
        #        print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno), end = '')
        #else:
        #    print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno), end = '')
        if event == 'line':
            print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno), end = '')
            self.logic_checker.check_conditions({}, scopes=self.CactusStack.current_frame.vars)
        # wait for command
        self.WaitUntil(1)

        # print command, should be event == line or call
        print('innerFunction(): ', self.command)

        # the initial stepover command may be detected here
        # during line event processing
        if event == 'line':
            if self.command == 'stepover':
                # if this is the initial stepover command
                # initialize variables for mainTracer to handle
                # following call event
                if self.stepover_active == False:
                    self.stepover_active = True
                    self.stepover_call_depth = 0
                # innerFunctionStepover() detects command complete
                return

        if event == 'return' and frame.f_code.co_name != '<module>':
            print("innerFunction return pop node ", frame.f_code.co_name)
            self.logic_checker.check_conditions({}, scopes=self.CactusStack.current_frame.vars)
            self.CactusStack.pop()
        elif event == "return" and frame.f_code.co_name == '<module>':
            self.Set(0)
            return
        if self.quitValue == 1:
            print("innerFunction quitValue ", frame.f_code.co_name)
            #self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
            self.Set(0)
            raise SystemExit()

        self.Set(0)

    def innerFunctionStepover(self, frame, event, arg):
        '''
            This is a settrace() local callback function.  This callback persists
            for the duration of the current frame; that is, for the current function.
            After processing a return event, the global callback again becomes
            active.

            :param frame: frame object
            :param event String: "line", "return", "exception", "opcode"
            :param arg:
            :return:    settrace() local callback function
        '''
        self.curFrame = frame
        self.curEvent = event
        print('innerFunctionStepover(): ', event, frame.f_code.co_name, self.command)
        if event == 'line':
            print(str(frame.f_lineno) + '\t' + linecache.getline(self.filepath[1:], frame.f_lineno), end = '')

        if event == 'return' and frame.f_code.co_name != '<module>':
            print("innerFunctionStepover return pop node ", frame.f_code.co_name)
            self.logic_checker.check_conditions({}, scopes=self.CactusStack.current_frame.vars)
            self.CactusStack.pop()

        if event == 'return':
            if self.stepover_call_depth > 0:
                self.stepover_call_depth -= 1
                # if the call deptj is 0,
                # then this return indicates the end of the stepover
                if self.stepover_call_depth == 0:
                    self.stepover_active = False
                    # indicate that stepover command is complete
                    self.Set(0)
            else:
                print('inner function stepover ERROR')

    def TracerThread(self):
        self.injectTracer()

    def start(self):
        self.reset()
        t1 = threading.Thread(name='TracerThread', target=self.TracerThread)
        t1.start()
        self.threads = t1

    def quitEndProgram(self):
        self.commandHandler('quit')

    def quit(self):
        #settrace(None)
        self.WaitUntil(0)
        self.quitValue = 1
        self.command = 'quit'
        self.Set(1)
        self.WaitUntil(0)
        # clearing stops callbacks
        settrace(None)

        try:
            self.threads.join()
            print("\nlogic checker results")
            self.logic_checker.program_end({}, scopes=self.CactusStack.current_frame.vars)
            # self.reset()
        except:
            print("Error: Used quit without a corresponding start. Please use start to begin trace.")

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
#        if self.curFrame is not None and (int(self.lastlineofprogram) <= int(self.curFrame.f_lineno)):
#            print("reached last line of file")
#            self.quit()
#        elif command == 'quit':
        if command == 'quit':
            self.quit()
        else:
            self.WaitUntil(0)
            self.command = command
            self.Set(1)

    def step(self):
        newCommand = "step"
        self.commandHandler(newCommand)

    def stepover(self):
        if self.curEvent == 'call' or self.curEvent == 'line':
            newCommand = "stepover"
            self.commandHandler(newCommand)
        else:
            print('can not stepover because not over function')

    def continueRun(self):
        if self.curFrame == None:
            self.step()
        self.WaitUntil(0)
        # if self.curFrame.f_lineno == 1:
        #     self.step()
        #print(linecache.getline(self.curFrame.f_code.co_name, self.curFrame.f_lineno))
        while self.curFrame.f_lineno not in self.breakpointlist and self.curFrame.f_lineno != self.lastlineofprogram:
            # print(self.curFrame.f_lineno)
            self.commandHandler('step')
        #self.step()

    def addbreakpoint(self, breakpointNew):
        for breakpointElement in breakpointNew:
            self.breakpointlist.append(breakpointElement)

    def removebreakpoint(self, breakpointToRemove):
        self.breakpointlist.remove(breakpointToRemove)
    
    def printScopeTree(self):
        #self.WaitUntil(0)
        print(self.CactusStack.print_tree())
        self.CactusStack.print_frame()