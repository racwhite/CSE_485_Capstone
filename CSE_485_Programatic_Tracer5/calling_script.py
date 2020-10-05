#!/usr/bin/env python3

import myscript4

thing1 = myscript4.Python_tacer()
#thing1.setFilePath("/test/myscript2.py")
thing1.watchVar("a")
thing1.watchVar("d")
#thing1.exec_steps('for')
#thing1.setFilePath("/test/brokentest.py")
#thing1.exec_steps('for')
thing1.setFilePath("/test/functioncalls.py")
thing1.exec_steps('for')
thing1.setFilePath("/test/helloworld.py")
thing1.exec_steps('for')
thing1.setFilePath("/test/recursivefunction.py")
thing1.exec_steps('for')
thing1.setFilePath("/test/syntaxerror.py")
thing1.exec_steps('for')
thing1.setFilePath("/test/variableassignment.py")
