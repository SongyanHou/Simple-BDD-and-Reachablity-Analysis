README
Author: Songyan Hou (sh3348)

There are two Python source code files: 
BinaryDecisionDiagram.py -- BDD package
Reachability.py -- Used for analyzing the reachability of given systems

To test the BDD package, we need to start python running environment first.

Example:
%python
Python 2.7.5 (default, Mar  9 2014, 22:15:05) 
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import BinaryDecisionDiagram as BDD
>>> bdd=BDD.BinaryDecisionDiagram()
>>>
>>> #Create New Variables
>>> x=bdd.newVariable("x")
>>> y=bdd.newVariable("y")
>>>
>>> r1=bdd.apply_and(x,y)
>>> r1.printTree()
('', <DiagramNode: x>)
('\t', <DiagramNode: y>)
('\t\t', <TerminalNode: True>)
('\t\t', <TerminalNode: False>)
('\t', <TerminalNode: False>)
>>>
>>> r2=bdd.apply_xor(x,y)
>>> r2.printTree()
('', <DiagramNode: x>)
('\t', <DiagramNode: y>)
('\t\t', <TerminalNode: False>)
('\t\t', <TerminalNode: True>)
('\t', <DiagramNode: y>)
('\t\t', <TerminalNode: True>)
('\t\t', <TerminalNode: False>)
>>>
>>>
>>> print r1==r2
False
>>>quit()


To check the reachability of test systems, the reachability.py should be invoked in terminal as:
%python reachability.py test1.txt 1
OR
%python reachability.py test2.txt 2

There are two arguments in the command: first one is the name of test system file, and the second is the running option. 

option 1 indicates checking bad state only and terminate the program after a bad state is detected. All reachable states before the bad state is detected are printed out.

option 2 indicates checking all reachable states. The program keeps running even after the bad state is detected and all reachable states of this system will be printed out after program terminates.

The zip file contains two test system files: test 1.txt represents a system with 14 states and 30 transitions; test 2.txt represents a system with 1000 states and 10001 transitions. Bad state is reachable in both systems.
