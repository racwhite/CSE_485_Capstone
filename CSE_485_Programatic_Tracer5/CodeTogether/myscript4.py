#!/usr/bin/env python3

#from cactus import Node
import analysis3
import importlib.util
from sys import settrace
import sys
import linecache
import os
import io
import inspect
import threading

class Python_tacer():



    def __init__(self):

        self.filepath_var = ""
        self.local_vars = {}
        self.t = []
        self.tvalue = {}
        self.function_watch = ""
        self.start = 0
        self.cur_frame = ""
        self.previous_line = ""
        self.skipline = False
        self.skipfunction = ""
        self.skipinnerline = False
        self.skipinnerfunction = ""
        self.previous_command = "s"
        self.output = ""
        self.list_lines = True
        self.break_line = 1
        self.return_present = False
        self.end = None
        self.keyword_count = 0
        self.keyword_lineno = ""
        self.keyword = ""
        self.keywords = ""
        self.continue_code = False
        self.step = []
        self.command_index = 0
        self.initial_run = 0
        self.flag = 2
        self.breakpointlist = []
        self.cur_event = 0
        self.quit_value = 0
        self.oldline = ""
        #self.localStorage = threading.local()
        #self.localStorage.step = []
        #self.localStorage.command_index = 0

        self.var = 0
        self.var_mutex = threading.Lock()
        self.var_event = threading.Event()

        #self.CactusStack = None

    """
    This function does nothing and is not used in the code
    """
    def clear_set(self):
        self.initial_run = 0
        self.flag = 2
        self.step = []
        self.command_index = 0

    """
    This function sets the filepath_var attribute of the class to the string "filepath_set"
    that gets passed to the function 
    """
    def setFilePath(self, filepath_set):
        self.filepath_var = filepath_set

    """
    This function calls exec() on the compiled target code and is called in the thread1.
    It takes a keyword string (not used) and a varWatchList list (set to None and not used).
    """
    def exec_steps(self, keyword, varWatchList=None):
        self.initial_run = 0
        self.keywords = keyword
        globals = {}
        path = os.getcwd()+self.filepath_var
        with open(path, 'rb') as file:
            tracer_func = self.my_tracer6
            globals.update({
            "__name__": "__main__",
            })
            thing5 = compile(file.read(), path,'exec')
            settrace(tracer_func)
            self.flag = 0
            exec(thing5, globals, None)
            # try:
            #     exec(thing5, globals, None)
            # except Exception as e:
            #     print(e)
            #     print("Something went wrong. Currently in exec_steps")
                
            self.flag = 1

            settrace(None)

    """
    Main loop of the debugger and main tracer function. Has parameters of frame, (frame object),
    event, (String), and arg (arguments) 
    """
    def my_tracer6(self, frame, event, arg):

        #make sure to uncomment
        self.cur_frame = frame
        # if(self.CactusStack is None or self.CactusStack.is_empty()):
        #     self.CactusStack = Node(frame.f_code.co_name, frame.f_locals)
        #     self.CactusStack.reset_scopes()
        #     Node.scopes = [frame.f_code.co_name]
        #     del self.CactusStack.current_frame.vars['__builtins__']
        #     print(self.CactusStack.print_tree())
        # else:
        #     self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
        #     print(self.CactusStack.print_tree())

        if event == 'call':
            print("my_tracer6 cur_event = -1")
            self.cur_event = -1
        else:
            print("my_tracer6 cur_event =  0")
            self.cur_event = 0

        if event == "return" and frame.f_code.co_name == self.skipfunction and self.skipfunction != "<module>":
            self.skipline = False
            self.skipfunction = ""            

        # following line will abort trace if filename changes, consider this before implementing/reimplementing
        # if frame.f_code.co_filename != os.getcwd()+self.filepath_var:
        #     settrace(None)
        length_file = len(self.filepath_var)

        length_file = len(self.filepath_var)
        if self.skipline != True:
            command = "s"
        else:
            command = "ss"

        if event == "call" or event == "return" or event == "line":
            if command is "s":
                if event == "return":
                    self.lines(frame, event)
                    #print("got here in self.my_tracer6")
                    self.my_tracer6
                    #return self.func6(frame.f_back, event ,arg)
                else:
                    return self.func6
            else:
                self.lines(frame, event)
                return self.my_tracer6
        self.lines(frame, event)
        return self.my_tracer6

    """
    This fucntion is run when the command is 'n' and is called from func6.
    Has parameters of frame, (frame object),event, (String), and arg (arguments).
    """
    def step_over(self, frame, event, arg):
        if self.skipline == False:
            self.lines(frame, event)
        if event == "return":
            self.lines(frame, event)
            return self.my_tracer6
        return self.my_tracer6

    """
    This fucntion is run when the command is 'n' and is called from func6.
    Has parameters of frame, (frame object),event, (String), and arg (arguments).
    """
    def func6(self,frame, event, arg):
        self.cur_frame = frame
        self.skipline = False
        length_file = len(self.filepath_var)
        filename = self.filepath_var[1:length_file]
        if self.initial_run != 0:
            print(self.oldline)
        else:
            pass

        #f = inspect.currentframe()
        frame2 = sys._current_frames().get(threading.get_ident(), None)
        #line = linecache.getline(frame2.f_code.co_filename, frame2.f_lineno)  
        
        line = linecache.getline(filename, frame.f_lineno)
        self.oldline = line

        self.continue_code = False
        self.lines(frame, event)            
        self.Set(0)
        if self.quit_value == 1:
            raise SystemExit()
        self.WaitUntil(1)
        
        # if event == 'call':
        #     print("func6 cur_event = -1")
        #     self.cur_event = -1
        # else:
        #     print("func6 cur_event =  0")
        #     self.cur_event = 0

        #print("func6 cur_event = 0")
        #self.cur_event = 0
        self.initial_run = self.initial_run + 1
        command2 = self.command_func(self.step[self.command_index],frame,event)
        #print(self.step)

        self.step[self.command_index] = ''
        for i in range(len(self.step)-(self.command_index+1)):
            #print(i)
            self.step.remove(self.step[self.command_index+i])

        self.command_index = self.command_index + 1     


        if command2 == 's':
            return self.func6
        else:
            self.skipline = True
            self.skipfunction = frame.f_code.co_name
            return self.step_over

    """
    This function is for debugging purposes and to update CactusStack. It returns string values based on the command buffers
    current state. Has parameters of frame, (frame object),event, (String), and arg (arguments).
    """
    def command_func(self, command, frame, event):
        #make sure to uncomment
        # if not self.CactusStack.is_empty():
        #     print(self.CactusStack.print_tree())
        if command == "":
            return self.previous_command
        if command[0] == "p":
            pass
        if command[0] == "s":
            #print("command = ", command[0])            
            return "s"
        if command[0] == "n":
            return "n"
        return "s"

    """
    This function is for debugging purposes and to update CactusStack. It returns string values based on the command buffers
    current state. Has parameters of frame, (frame object), and event, (String).
    """
    def lines(self, frame, event):
        # make sure to uncomment
        # if event == 'return':
        #     self.CactusStack.pop()
        #     print(self.CactusStack.print_tree())
        if self.list_lines == True:
            length_file = len(self.filepath_var)
            filename = self.filepath_var[1:length_file]
            i = 0
            code = ""
            line = ""
            for i in range(frame.f_code.co_firstlineno,frame.f_lineno + 5):
                line = linecache.getline(filename, i)
                if linecache.getline(filename, frame.f_lineno).strip()[0:7] == 'return ':
                    self.return_present = True
                if line != None and line != "":
                    if frame.f_lineno == i:
                        code +=  str(i) + " -->" + line
                    else:
                        code +=  str(i) + "    " + line
                else:
                    code += ""
                    if self.end is None:
                        self.end = frame.f_lineno - 4

            # saving these print statements for debug purposes later
            # print("----------------next lines-------------\n\n" + "*** IN " + frame.f_code.co_name + " ***\n" + code)
            # print("----------------program output --------\n\n")
        else:
            length_file = len(self.filepath_var)
            filename = self.filepath_var[1:length_file]
            line = linecache.getline(filename, frame.f_lineno)
            code = "line: " + str(frame.f_lineno) + " -->" + line.strip()
            # print("----------------next lines-------------\n\n" + "*** IN " + frame.f_code.co_name + " ***\n" + code)
            # print("----------------program output --------\n\n")

    """
    This function is for adding a step or 's' command to buffer. Has parameters of frame, (frame object),event,
    (String), and arg (arguments).
    """
    def step1(self):
        self.step.append('s')

    """
    This function is for adding a next or 'n' command to buffer. Has parameters of frame, (frame object),event,
    (String), and arg (arguments).
    """
    def next1(self):
        self.step.append('n')

    """
    This function is for waiting untill a certain lock state is aqquired. Has parameters of v (int).
    """
    def WaitUntil(self, v):
        while True:
            self.var_mutex.acquire()
            if self.var == v:
                self.var_mutex.release()
                return # Done waiting
            self.var_mutex.release()
            self.var_event.wait(1) # Wait 1 sec

    """
    This function is for setting a certain lock state v. Has parameters of v (int).
    """
    def Set(self, v):
        self.var_mutex.acquire()
        self.var = v
        self.var_mutex.release()
        self.var_event.set() # In case someone is waiting
        self.var_event.clear()

    """
    This fuction is a "reset" for the debugger. has no parameters. needs to be updated eventually.
    """
    def reset_steplist(self):
        self.quit_value = 0
        self.breakpointlist = []
        #print("In reset_steplist")
        #print("Command index is " + str(self.command_index))
        #self.step = []
        #print("Step contains: ")
        #print(', '.join(str(step)))
        self.command_index = 0
        self.step = ['s']
        #print("Command index is " + str(self.command_index))
        #self.step = []
        #print("Step contains: ")
        #print(', '.join(str(step)))
        #print(self.step)

"""
This is the main object instantiation of the Python_tracer class.
"""
thing1 = Python_tacer()
"""
this is the Threads array for housing thread1.
"""
threads = ['']

"""
This fuction takes no parameters and is the implementation of the static analysis.
"""
def analysis():
    AsseMbly=analysis3.Assembly()
    SourceProgram=[]
    Filepath= os.getcwd() + "/target_code/myscript2.py"
    for line in open(Filepath,'r',encoding='UTF-8-sig' ):
        line=line.replace('\n','')
        SourceProgram.append(line)
    print(SourceProgram)
    SourceProgram=AsseMbly.DeleteNote(SourceProgram)
    print(SourceProgram)
    SourceProgram=AsseMbly.PassSpace(SourceProgram)
    SourceProgram=AsseMbly.Reader(SourceProgram)
    print(SourceProgram)
    AsseMbly.JugeMent(SourceProgram)

"""
This code is the way to quit out of an execution of a specific target code.
This takes no parameters and is necessary to run to change the target code execution.
"""
def quit():
    thing1.WaitUntil(0)
    settrace(None)

    thing1.step1()
    thing1.step1()
    thing1.quit_value = 1
    thing1.Set(1)
    threads[0].join()

"""Executes one line of code. No parameters"""
def step():
    thing1.WaitUntil(0)
    #print(thing1.cur_event)
    #print("thing1.command_index = ", thing1.command_index)
    #print("num of threads = ", threading.active_count())
    # line = ""
    # line = linecache.getline(thing1.filepath_var[1:], thing1.cur_frame.f_lineno-1)
    # print("lineno = ", thing1.cur_frame.f_lineno-1)
    thing1.step1()
    thing1.Set(1)

"""Appends a list of ints to the breakpoint list. parameters of linenumber (List)"""
def addbreakpoint(linenumber):
    for item in linenumber:
        thing1.breakpointlist.append(item)

"""Runs the program until it hits a breakpoint. No parameters"""
def continue_run():
    step()
    breakpoint(thing1.breakpointlist)

"""Helper function for continue_run. Parameter of linenumberlist (list of ints)"""
def breakpoint(linenumberlist):
    #print("num of threads = ", threading.active_count())
    line = ""
    while thing1.cur_frame.f_lineno-1 not in linenumberlist:
        step()
        line = linecache.getline(thing1.filepath_var[1:], thing1.cur_frame.f_lineno-1)
        print("line = ", line)
        print("lineno = ", thing1.cur_frame.f_lineno-1)
"""
Implements stepout functionality of the debugger. No parameters
"""
def stepout():
    thing1.WaitUntil(0)
    thing1.next1()
    thing1.Set(1)

"""
Implements stepover functionality of the debugger. No parameters
corner case: calling stepover while not over function doesn't work as intended
"""
def stepover():
    thing1.WaitUntil(0)  
    print("cur_event = ",thing1.cur_event)
    line = ""
    if thing1.cur_event != -1:
        print("step instead of stepover")
        line = linecache.getline(thing1.filepath_var[1:], thing1.cur_frame.f_lineno-1)
        print("lineno = ", thing1.cur_frame.f_lineno-1)
        step()
    else:        
        #step()
        step()
        print("after step in stepover")
        line = linecache.getline(thing1.filepath_var[1:], thing1.cur_frame.f_lineno-1)
        print("lineno = ", thing1.cur_frame.f_lineno-1)
        stepout()
        print("lineno = ", thing1.cur_frame.f_lineno-1)
        #thing1.Set(1)
        step()
    #thing1.Set(1)

        #previous working try!!!!!!!!!!!!!!!!!! save this just in case, for now
        # print(thing1.cur_frame.f_lineno)
        # function_name = thing1.cur_frame.f_code.co_name
        # print(thing1.cur_frame.f_code.co_name)
        # while function_name == thing1.cur_frame.f_code.co_name:
        #     print(thing1.cur_frame.f_code.co_name)
        #     step()
        # print(str(thing1.cur_frame.f_lineno) + "end while")

"""Removes a breakpoint. Has a parameter breakpointtoremove (int)"""
def removebreakpoint(breakpointtoremove):
    thing1.breakpointlist.remove(breakpointtoremove)

"""
Main debugging thread for the debugger. No parameters
"""
def Thread1():
    thing1.WaitUntil(1)
    thing1.exec_steps('for')
    
"""
Begins executing a thread (a program) assuming that the target has been set. No parameters.
"""
def start():
    thing1.reset_steplist()
    t1 = threading.Thread(name='Thread1', target=Thread1)
    #t_test = threading.get_ident()
    #print("thread name = ", t_test)
    t1.start()
    threads[0] = t1