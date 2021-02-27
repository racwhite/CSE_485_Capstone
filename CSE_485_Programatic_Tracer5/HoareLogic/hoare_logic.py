#!/usr/bin/env python3

import sys

class program_conditions:

    # Initialize all the data structures
    def __init__(self,filename):

        self.pre_cond = {}
        self.post_cond = {}
        self.message = {}
        self.pre_bool = {}
        self.post_bool = {}
        self.full_length = 0

        with open (filename) as cond:
            self.conditions = cond.read().splitlines()

        for line in self.conditions:
            splitted = line.split(';')
            self.pre_cond[self.full_length] = splitted[0]
            self.post_cond[self.full_length] = splitted[1]
            self.message[self.full_length] = splitted[2].replace('"', '')
            self.pre_bool[self.full_length] = False
            self.post_bool[self.full_length] = False
            self.full_length = self.full_length + 1


    # Create check_conditions(), where after every step of the program, the conditions should be checked
    def check_conditions(self, global_scope, scopes):
        recheck = False
        for i in range(0,self.full_length):
            # Traverse through all conditions
            if (self.pre_bool[i] == False):
                # Pre condition was not met yet
                # Identify type of operator in pre_cond

                result = self.compare_vars(global_scope, scopes, self.pre_cond[i], i+1)
                if (result):
                    self.pre_bool[i] = True
                    recheck = True

            if (self.pre_bool[i] and self.post_bool[i] == False): # Pre condition was met & Post condition is false
                # Given the position i, find if the post condition was met
                # Identify type of operator in post_cond

                result = self.compare_vars(global_scope, scopes, self.post_cond[i], i+1)
                if (result):
                    self.post_bool[i] = True
                    recheck = True

        if (recheck):
            self.check_conditions(global_scope,scopes)

    # Create program_end(), where if the program ends, verify if all the conditions are met
    def program_end(self,global_scope,scopes):
        self.check_conditions(global_scope,scopes)
        # Iterate through post_bool and scan for any false
        false_found = False
        index = 0
        for i in range(0,self.full_length):
            # Old print message
            # print("Condition",(i+1),":",self.post_bool[i])
            if(self.post_bool[i] == False and false_found == False):
                false_found = True
                index = i
        if(false_found):
            # A condition was not met
            print(self.message[index])
        else:
            # All the conditions were met
            print("All of the provided conditions were met.")

    def compare_vars(self, global_scope, scopes, cond, num):

        evalResult = eval(cond,global_scope,scopes)

        # Confirm that evalResult is a boolean and therefore the condition is a boolean expression
        if(evalResult==True):
            return True
        elif(evalResult==False):
            return False
        else:
            print("Error: The evaluation of line",num,"did not result in a boolean")
            sys.exit()
