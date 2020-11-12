#!/usr/bin/env python3

from cactus import Node
import analysis3
import importlib.util
#from importlib import util
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
        #count = []
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

        self.var = 0
        self.var_mutex = threading.Lock()
        self.var_event = threading.Event()

        self.CactusStack = None

    def clear_set(self):
        self.initial_run = 0
        self.flag = 2
        self.step = []
        self.command_index = 0

    def setFilePath(self, filepath_set):
        self.filepath_var = filepath_set

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
            # except:
            #     print("Something went wrong. Currently in exec_steps")
            #     pass
            self.flag = 1

            settrace(None)

    def my_tracer6(self, frame, event, arg):
        
        self.cur_frame = frame
        if(self.CactusStack is None or self.CactusStack.is_empty()):
            self.CactusStack = Node(frame.f_code.co_name, frame.f_locals)
            self.CactusStack.reset_scopes()
            Node.scopes = [frame.f_code.co_name]
            del self.CactusStack.current_frame.vars['__builtins__']
            print(self.CactusStack.print_tree())
        else:
            self.CactusStack.push(Node(frame.f_code.co_name, frame.f_locals))
            print(self.CactusStack.print_tree())

        # if event == 'call':
        #      self.cur_event = 1
        #self.cur_event = self.cur_event.replace(self.cur_event[0:],event)
        #self.command_index = self.command_index + 1

        if event == 'call':
            self.cur_event = -1
        else:
            self.cur_event = 0

        if event == "return" and frame.f_code.co_name == self.skipfunction and self.skipfunction != "<module>":
            self.skipline = False
            self.skipfunction = ""
            #self.skipinnerline = False

        # following line will abort trace if filename changes, consider this before implementing/reimplementing
        # if frame.f_code.co_filename != os.getcwd()+self.filepath_var:
        #     settrace(None)
        length_file = len(self.filepath_var)
        #filename = self.filepath_var[1:length_file]
        #self.print_Local_vars(frame, event, arg)

        length_file = len(self.filepath_var)
        if self.skipline != True:
            command = "s"
        else:
            command = "ss"

        if event == "call" or event == "return" or event == "line":
            if command is "s":
                if event == "return":
                    #print("got here in self.my_tracer6")
                    self.my_tracer6
                    #return self.func6(frame.f_back, event ,arg)
                else:
                    return self.func6
            else:
                return self.my_tracer6
        self.lines(frame, event)
        return self.my_tracer6

    def step_over(self, frame, event, arg):
        #self.print_Local_vars(frame, event, arg)
        if self.skipline == False:
            self.lines(frame, event)
        if event == "return":
            #print("Here")
            return self.my_tracer6
        return self.my_tracer6

    def func6(self,frame, event, arg):
        # self.cur_event = event
        #self.cur_event = self.cur_event.replace(self.cur_event[0:],event)
        # if event == 'call':
        #     self.cur_event = -1
        # else:
        #     self.cur_event = 0
        # if self.cur_event < 2:
        #     self.cur_event = self.cur_event + 1
        self.cur_frame = frame
        self.skipline = False
        length_file = len(self.filepath_var)
        filename = self.filepath_var[1:length_file]
        line = linecache.getline(filename, frame.f_lineno)
        if self.skipinnerline != True:
            self.continue_code = False
            self.lines(frame, event)
            print(line)
            #if self.initial_run != 0:
            #self.step[self.command_index] = ''
                #print(line)
            self.Set(0)
            if self.quit_value == 1:
                raise SystemExit()
            self.WaitUntil(1)
            self.cur_event = 0
            #else:
            #self.initial_run = self.initial_run + 1
            command2 = self.command_func(self.step[self.command_index],frame,event)
            print(self.step)

            self.step[self.command_index] = ''
            for i in range(len(self.step)-(self.command_index+1)):
                print(i)
                self.step.remove(self.step[self.command_index+i])

            #if self.command_index < (len(self.step) - 1):
            self.command_index = self.command_index + 1
            #self.command_index = self.command_index + 1
            #print(line)
            #command2 = self.command_func(input("***Prompt***\n" + path + "\n(PTR)"), frame, event)
            print("\n")
        else:
            command2 = "ss"
        if command2 == 's':
            #self.print_Local_vars(frame, event, arg)
            return self.func6
        else:
            #self.print_Local_vars(frame, event, arg)
            self.skipline = True
            self.skipfunction = frame.f_code.co_name
            return self.step_over

    def command_func(self, command, frame, event):
        if not self.CactusStack.is_empty():
            print(self.CactusStack.print_tree())
        if command == "":
            return self.previous_command
        if command[0] == "p":
            pass
        if command[0] == "s":
            #settrace(None);
            return "s"
        if command[0] == "n":
            return "n"
        return "s"

    def lines(self, frame, event):
        if event == 'return':
            self.CactusStack.pop()
            print(self.CactusStack.print_tree())
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

            # print("----------------next lines-------------\n\n" + "*** IN " + frame.f_code.co_name + " ***\n" + code)
            # print("----------------program output --------\n\n")
        else:
            length_file = len(self.filepath_var)
            filename = self.filepath_var[1:length_file]
            line = linecache.getline(filename, frame.f_lineno)
            code = "line: " + str(frame.f_lineno) + " -->" + line.strip()
            # print("----------------next lines-------------\n\n" + "*** IN " + frame.f_code.co_name + " ***\n" + code)
            # print("----------------program output --------\n\n")


    def step1(self):
        self.step.append('s')


    def next1(self):
        self.step.append('n')


    def WaitUntil(self, v):
        while True:
            self.var_mutex.acquire()
            if self.var == v:
                self.var_mutex.release()
                return # Done waiting
            self.var_mutex.release()
            self.var_event.wait(1) # Wait 1 sec

    def Set(self, v):
        self.var_mutex.acquire()
        self.var = v
        self.var_mutex.release()
        self.var_event.set() # In case someone is waiting
        self.var_event.clear()

    def reset_steplist(self):
        self.quit_value = 0
        self.breakpointlist = []
        print("In reset_steplist")
        print("Command index is " + str(self.command_index))
        #self.step = []
        print("Step contains: ")
        print(', '.join(str(step)))
        self.command_index = 0
        self.step = ['s']
        print("Command index is " + str(self.command_index))
        #self.step = []
        print("Step contains: ")
        #print(', '.join(str(step)))
        print(self.step)


thing1 = Python_tacer()
threads = ['']

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

def quit():
    thing1.WaitUntil(0)
    settrace(None)

    #step()
    #step()
    thing1.step1()
    thing1.step1()
    thing1.quit_value = 1
    #time.sleep(1)
    thing1.Set(1)
    print("before join")
    threads[0].join()
    #step()
    #step()
    print("after join")


def step():
    thing1.WaitUntil(0)
    print(thing1.cur_event)
    print("thing1.command_index = ", thing1.command_index)
    print("num of threads = ", threading.active_count())
    thing1.step1()
    thing1.Set(1)

def addbreakpoint(linenumber):
    for item in linenumber:
        thing1.breakpointlist.append(item)

def continue_run():
    step()
    breakpoint(thing1.breakpointlist)

def breakpoint(linenumberlist):
    #thing1.WaitUntil(0)
    print("num of threads = ", threading.active_count())
    line = ""
    while thing1.cur_frame.f_lineno not in linenumberlist:
    #for i in range(5):
        step()
        line = linecache.getline(thing1.filepath_var[1:], thing1.cur_frame.f_lineno)
        print("line = ", line)
        print("lineno = ", thing1.cur_frame.f_lineno)
    #thing1.Set(1)

def stepout():
    thing1.WaitUntil(0)
    thing1.next1()
    thing1.Set(1)

def stepover():
    #print(type(thing1.cur_frame.f_lineno))
    #breakline = thing1.cur_frame.f_lineno + 1
    #addbreakpoint([breakline])
    #continue_run()
    #removebreakpoint(breakline)
    #corner case of calling stepover while not over function
    print("cur_event = ",thing1.cur_event)
    if thing1.cur_event != -1:
        step()
    else:
        #step()
        step()
        stepout()
        #step()
        #previous working try!!!!!!!!!!!!!!!!!!
        # print(thing1.cur_frame.f_lineno)
        # function_name = thing1.cur_frame.f_code.co_name
        # print(thing1.cur_frame.f_code.co_name)
        # while function_name == thing1.cur_frame.f_code.co_name:
        #     print(thing1.cur_frame.f_code.co_name)
        #     step()
        # print(str(thing1.cur_frame.f_lineno) + "end while")

def removebreakpoint(breakpointtoremove):
    thing1.breakpointlist.remove(breakpointtoremove)

# def Thread0():
#     #thing1.WaitUntil(0)
#     print("")

def Thread1():
    thing1.WaitUntil(1)
    #while True:
    #while thing1.flag == 0:
    #     time.sleep(.0001)
    thing1.exec_steps('for')
    #thing1.step1()

def start():
    thing1.reset_steplist()
    #threading.Thread(name='Thread1', target=Thread1).start()
    #t3 = threading.Thread(name='Thread2', target=Thread2).start()
    t1 = threading.Thread(name='Thread1', target=Thread1)
    t1.start()
    threads[0] = t1
    #print(threads[0].is_alive())
    #print(threads[0])
    #t3 = threading.Thread(name='Thread2', target=Thread2).start()
