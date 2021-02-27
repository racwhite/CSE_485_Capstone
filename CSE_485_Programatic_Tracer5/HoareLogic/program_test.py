#!/usr/bin/env python3

import hoare_logic

#simulate the actions of a real program
#call functions and send scopes


autograder = hoare_logic.program_conditions("conditions.txt")

global_vars = {'x' : 1}

scope1 = {'a' : 0, 'b' : 0, 'c' : 0}
autograder.check_conditions(global_vars,scope1)

scope1 = {'a' : 1, 'b' : 0, 'c' : 0}
autograder.check_conditions(global_vars,scope1)

scope1 = {'a' : 1, 'b' : 2, 'c' : 0}
autograder.check_conditions(global_vars,scope1)

scope1 = {'a' : 1, 'b' : 2, 'c' : 3}
autograder.check_conditions(global_vars,scope1)

autograder.program_end(global_vars,scope1)
