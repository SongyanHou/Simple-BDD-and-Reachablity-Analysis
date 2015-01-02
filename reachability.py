# encoding: utf-8
'''
Date: 2014/12/18

@authors: Songyan Hou/Linyin Wu
'''

import math
import sys 
import time
import BinaryDecisionDiagram as BDD

bdd = BDD.BinaryDecisionDiagram()

def DecToBin(integer):
#convert decimal to binary list
	bin = []
	quotient = integer
	for i in range(num):
		remainder = quotient%2				
		bin.append(remainder)				
		quotient = quotient/2
	return bin

def BinToState(bin):
#translate binary list to state
	root = BDD.TermNode(True)	
	for i in range(len(bin)):
		if bin[i]==0:
			root=bdd.apply_and(root, bdd.apply_not(list[i]))
		else:
			root=bdd.apply_and(root, list[i])
	return root

if __name__ == '__main__':
	if len(sys.argv)!=3:
		print "Wrong Input Format!"
		print "Usage: python reachability.py filename option (1--just check bad state; 2--show all reachable states)"
		exit(1)
	filename = sys.argv[1]
	choice =int (sys.argv[2])

	#open file get n m and the edge
	file = open(filename, 'r')	
	tmp = file.readline()
	tmp = tmp.strip()
	tmp = tmp.split()
	n = int(tmp[0])
	m = int(tmp[1])
	lines = file.readlines()
	file.close()

	num = int(math.ceil(math.log(n)/math.log(2)))

	list = []
	for i in range(num):
		list.append(bdd.newVariable(chr(ord("a")+i)))

	#the initial state is s0
	s0_bin = []
	for i in range(num):
		s0_bin.append(0)
	sx = BinToState(s0_bin)

	#the bad state is s1
	s1_bin = []			
	s1_bin.append(1)
	for i in range(num-1):
		s1_bin.append(0)
	s1_state = BinToState(s1_bin)

	reachPoint=[0]		
	#list recording all reachable states

	bad_flag=False
	break_flag=False

	print "Start Time: "+time.strftime("%I:%M:%S", time.localtime(time.time()))+"\n"

	sx_tmp = 0
	while sx != sx_tmp and break_flag==False:	
	#check if fixpoint has been reached
		sx_tmp = sx
		for i in range(m):
		#go through the whole file, read the transition for each line
			tmp = lines[i]
			tmp = tmp.strip()
			tmp = tmp.split()
			s_dec = int(tmp[0])	
			# print s_dec
			s_bin = DecToBin(s_dec)
			# print s_bin
			s_state = BinToState(s_bin)
			test = bdd.apply_and(sx, s_state)
			if test == BDD.TermNode(False): 
			#if the start state has not been reached before, continue
				continue
			else:			
			#if the start state is reachable state, add destination state into reachable states set
				t_dec = int(tmp[1])
				for i in range(len(reachPoint)):
					if t_dec not in reachPoint:
						reachPoint.append(t_dec)

				t_bin = DecToBin(t_dec)
				t_state = BinToState(t_bin)
				if t_state==s1_state and bad_flag==False:	#check if this new state is bad state
					print "Time: "+time.strftime("%I:%M:%S", time.localtime(time.time()))
					print ":(\tThe bad state is reachable\n"
					bad_flag=True
					if choice==1:
						break_flag=True
						break
				sx = bdd.apply_or(sx, t_state)

	if bad_flag==False:
		print "Time: "+time.strftime("%I:%M:%S", time.localtime(time.time()))
		print ":)\tThe bad state is not reachable\n"
	
	if break_flag==False:
		print "Time: "+time.strftime("%I:%M:%S", time.localtime(time.time()))
		print "All points could be reached in this system start from state 0"
		print reachPoint
		print "\n\n"
	else:
		print "Time: "+time.strftime("%I:%M:%S", time.localtime(time.time()))
		print "The Program terminated when first bad state was detected"
		print "Before termination, all reachable states are:"
		print reachPoint
		print "\n\n"