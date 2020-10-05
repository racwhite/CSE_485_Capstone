#!/usr/bin/env python3

import importlib.util
#from importlib import util
from sys import settrace
import sys
import linecache
import os
import pdb
import ipdb
import myscript2
import io
import code
import inspect
import bdb
import cmd
import pprint
#import myscript2

class Python_tacer(pdb.Pdb):

    filepath_var = ""
    local_vars = {}
    t = []
    tvalue = {}
    #count = []
    function_watch = ""
    start = 0
    end = 0
    cur_frame = ""
    previous_line = ""
    skipline = False
    skipfunction = ""
    skipinnerline = False
    skipinnerfunction = ""
    previous_command = "s"
    output = ""
    stick_out = False
    list_lines = False
    break_line = 1
    num = 1
    return_present = False
    end = ""
    frame_thing = ""
    keyword_count = 0
    keyword_lineno = ""
    keyword = ""
    keywords = ""
    keywords_out = ""
    stick_keywords = False

    def __init__(self):
        filepath = ""

    def setFilePath(self, filepath_set):
        self.filepath_var = filepath_set
        self.Pdbn = pdb.Pdb()
        self.filename_test = ''
        #path = os.getcwd()+self.filepath_var
        #spec = importlib.util.spec_from_file_location("target", path)
        #foo = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(foo)

    def __print_Local_vars(self, frame, event, arg):
        for i in frame.f_locals:
            self.__updateVar(frame, i)
            self.__updateVal(frame, i)
            #print_var(frame, i)

    def __print_var(self, frame, tt):
        try:
            print("---------------var " + tt + "-------------")
            #print(frame.f_locals)
            #print(frame.f_globals)
            #print(tt)
            print(tt + " = " + str(frame.f_locals[tt]))
            #print(tt + " = ", frame.f_globals[tt] + "(var is global)")
            print("-----------------------------------")
        except:
            print("variable not local")
            #print("variable not global")
            print("-----------------------------------")
        try:
            for line in range(0,self.num):
                #print(line)
                print("\n")
                print("---------------var " + tt + "-------------")
                frame = frame.f_back
                print(tt + " = " + str(frame.f_locals[tt]) + "var in local-" + str(line+1))
                print("-----------------------------------")
        except:
            print("variable not in outer scope local-" + str(line+1))
            print("-----------------------------------")

    def __updateVar(self, frame, tt):
        if tt not in self.local_vars.keys():
            self.local_vars[tt] = frame.f_locals[tt]
            #i = 0
            # while self.local_vars[frame + i] in self.local_vars.keys():
            #     i = i + 1
            # self.local_vars[frame + i] = frame

    def __updateVal(self, frame, tt):
        if tt in self.t:
            if tt not in self.tvalue.keys():
                self.tvalue[tt] = frame.f_locals[tt]
                #print("var " + tt + " initialized to " + str(frame.f_locals[tt]))
                self.output += "line:   " + str(frame.f_lineno-1) + "    var " + tt + " initialized to " + str(frame.f_locals[tt]) +  "\n"
            else:
                if self.tvalue[tt] != frame.f_locals[tt]:
                    self.tvalue[tt] = frame.f_locals[tt]
                    self.output += "line:   " + str(frame.f_lineno-1) + "    var " + tt + " updated to " + str(frame.f_locals[tt]) + "\n"
                #else:
                    #print("same value " + tt + " = " + str(tvalue[tt]))

    def watchVar(self,tt):
        self.t.append(tt)


    def exec_trace(self):
        path = os.getcwd()+self.filepath_var
        os.system('python3 -m trace --trackcalls ' + path )
        os.system('python3 -m trace --listfuncs ' + path + ' | grep funcname:')
        os.system('python3 -m trace --count --summary ' + path)


    def exec_thing(self, path, file, tracer_func):
        globals = {}
        globals.update({
            "__name__": "__main__",
        })
        thing5 = compile(file.read(), path,'exec')
        # statement = "exec(compile(%r, %r, 'exec'))" % \
        #             (file.read(), path)
        settrace(tracer_func)
        exec(thing5, globals, None)


    def exec_steps(self, keyword, varWatchList=None):
        self.keywords = keyword
        globals = {}
        path = os.getcwd()+self.filepath_var
        with open(path, 'rb') as file:
            tracer_func = self.__my_tracer6
            self.exec_thing(path, file, tracer_func)
            print("----------------end output--------------")
            print(self.output)
            print("----------------end tracer--------------")
            settrace(None)
            #self.Pdbn.runcall(self.exec_thing, path, file)

    def __my_tracer6(self, frame, event, arg):
        if event == "return" and frame.f_code.co_name == self.skipfunction and self.skipfunction != "<module>":
            self.skipline = False
            self.skipfunction = ""
            #self.skipinnerline = False
        else:
            d = 2
        print(frame.f_code.co_filename)
        if frame.f_code.co_filename != os.getcwd()+self.filepath_var:
            settrace(None)
        print(event + frame.f_code.co_name )
        length_file = len(self.filepath_var)
        filename = self.filepath_var[1:length_file]
        self.check_for_keywords(self.keywords, frame, filename)
        self.__print_Local_vars(frame, event, arg)
        # extracts frame code
        code = frame.f_code
        # extracts calling function name
        func_name = code.co_name

        length_file = len(self.filepath_var)
        filename = self.filepath_var[1:length_file]
        line = linecache.getline(filename, frame.f_lineno)
        line_no = frame.f_lineno
        if self.skipline != True:
            command = "s"
        else:
            command = "ss"
        if frame != self.cur_frame:
            self.cur_frame = frame
            self.num = self.num + 1
        if event == "call" or event == "return" or event == "line":
            if command is "s":
                if event == "return":
                    print("got here in self.__my_tracer6")
                    self.__my_tracer6
                    return self.__func6(frame.f_back, event ,arg)
                else:
                    return self.__func6
            else:
                return self.__my_tracer6
        self.lines(frame, event)
        return self.__my_tracer6

    def step_over(self,frame,event, arg):
        self.__print_Local_vars(frame, event, arg)
        if self.skipline == False:
            self.lines(frame, event)
        if event == "return":
            print("Here")
            return self.__my_tracer6
        return self.__my_tracer6

    def step_over2(self,frame,event, arg):
        self.__print_Local_vars(frame, event, arg)
        if self.skipline == False:
             self.lines(frame, event)
        return None

    def __func6(self,frame, event, arg):
        self.skipline = False
        if frame != self.cur_frame:
            self.cur_frame = frame
            self.num = self.num + 1
        length_file = len(self.filepath_var)
        filename = self.filepath_var[1:length_file]
        line = linecache.getline(filename, frame.f_lineno)
        if self.skipinnerline != True:
            print("-------------------end output----------")
            #print(event)
            #print(self.end)
            self.lines(frame, event)
            #self.check_for_keywords(self.keywords, frame, filename)
            if self.stick_keywords == True:
                self.keywords_print_out(frame, filename)
            command2 = self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        else:
            command2 = "ss"
        if command2 == 's':
            print(line.strip()[0:6])
            self.__print_Local_vars(frame, event, arg)
            self.previous_line = line
            return self.__func6
        else:
            self.previous_line = line
            self.__print_Local_vars(frame, event, arg)
            self.skipline = True
            self.skipfunction = frame.f_code.co_name
            print(self.skipfunction)
            return self.step_over

    def command_func(self, command, frame, event):
        if command == "":
            return self.previous_command
        if command[0] == "p":
            if command[1:len(command)].strip(" ") == "out":
                print("--------------updated vars------------")
                if self.output == "":
                    print("None")
                else:
                    print(self.output)
                print("--------------------------------------")
            self.__print_var(frame,command[1:len(command)].strip(" "))
            self.command_func(input("(PTR)"), frame, event)
            self.previous_command = command
        if command == "sout":
            self.stick_out = True
            self.lines(frame, event)
            self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        if command == "qout":
            self.stick_out = False
            self.lines(frame, event)
            self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        if command == "list":
            self.list_lines = True
            self.lines(frame, event)
            self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        if command == "qlist":
            self.list_lines = False
            self.lines(frame, event)
            self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        if command == "skey":
            self.stick_keywords = True
            self.lines(frame, event)
            length_file = len(self.filepath_var)
            filename = self.filepath_var[1:length_file]
            self.keywords_print_out(frame, filename)
            self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        if command == "qkey":
            self.stick_keywords = False
            self.lines(frame, event)
            self.command_func(input("***Prompt***\n(PTR)"), frame, event)
        if command[0] == "s":
            return "s"
            self.previous_command = command
        if command[0] == "n":
            return "n"
            self.previous_command = command
        if command[0] == "b":
            self.break_line = 2
        return "s"

    def lines(self, frame, event):
        if self.stick_out == True:
            print("--------------updated vars------------\n\n")
            print(self.output)
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
                    if self.end == "":
                        self.end = frame.f_lineno - 4

            print("----------------next lines-------------\n\n" + "*** IN " + frame.f_code.co_name + " ***\n" + code)
            print("----------------program output --------\n\n")
        else:
            length_file = len(self.filepath_var)
            filename = self.filepath_var[1:length_file]
            line = linecache.getline(filename, frame.f_lineno)
            code = "line: " + str(frame.f_lineno) + " -->" + line.strip()
            print("----------------next lines-------------\n\n" + "*** IN " + frame.f_code.co_name + " ***\n" + code)
            print("----------------program output --------\n\n")
        self.frame_thing = frame

    def check_for_keywords(self, keywords, frame, filename):
        #for i in range(frame.f_code.co_firstlineno,frame.f_lineno + 5):
        line = linecache.getline(filename, frame.f_lineno)
        if linecache.getline(filename, frame.f_lineno).strip()[0:len(keywords)+1] == keywords + ' ':
            self.keyword = True
            self.keyword_lineno = frame.f_lineno
            self.keyword_count = self.keyword_count + 1
            self.keywords_out += str(self.keyword_lineno) + "   count = " + str(self.keyword_count) + " for keyword " + keywords + "\n"

    def keywords_print_out(self, frame, filename):
        print("-------------------key words-----------")
        self.check_for_keywords(self.keywords, frame, filename)
        print(self.keywords_out)
        print("----------------key words Done---------")
