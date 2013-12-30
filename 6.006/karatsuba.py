# This solution template should be turned in through our submission site, at
# https://alg.csail.mit.edu

######################################################################################
### WARNING:                                                                       ###
### Be sure to write the Python code yourself!  We do run sophisticated automated  ###
### comparisons between each pair of programs turned in.  We are saddened and      ###
### troubled each year when a few students turn in nearly identical programs, and  ###
### we have to administer appropriate consequences.  It is better to turn in a     ###
### statement that you didn't have time to complete the assignment than to turn in ###
### the same code as someone else.                                                 ###
######################################################################################

###################
### Problem 3-4 ###
###################

# NOTE: For naive_multiply and karatsuba_multiply, you may
# only use the Python "*" operator on single digit multiplications
# and on multiplying numbers by powers of 10. You may also use the 
# Python "**" operator.
# 
# In those two functions, all uses for "*" should be of the form 
# a * b (where a and b are single digit numbers)
# or 
# a * (10**b) (a and b don't need to be single digit numbers)

#===================
# Problem 3-4a
#===================
# This function naive_multiply takes in two integers (or longs)
# and multiplies them together using the Grade School
# Multiplication Algorithm.
#
# Remember to only use the Python "*" operator in the manner described above.

def naive_multiply(x, y):
	strx=str(x)
	stry=str(y)
	value=0
	for n in range(len(strx)):
		for m in range(len(stry)):
			prod = eval(strx[n]+"*"+stry[m])
			power=10**((len(strx)-n-1)+(len(stry)-m-1))
			value+=prod*power
	return value


#===================
# Problem 3-4c
#===================
# This function karatsuba_multiply takes in two integers (or longs)
# and multiplies them together using the Karatsuba
# Multiplication Algorithm.
#
# Remember to only use the Python "*" operator in the manner described above.

def karatsuba_multiply(x, y):
	#print "\nNEW"
	if x < 10 and y < 10:
		return x*y
	sx=str(x)
	sy=str(y)
	m = max(len(sx), len(sy))
	sx='0'*(m-len(sx))+sx
	sy='0'*(m-len(sy))+sy
	m1=(m+1)/2
	m2=m/2
	lox=int(sx[m1:])
	hix=int(sx[:m1])
	loy=int(sy[m1:])
	hiy=int(sy[:m1])
	z0 = karatsuba_multiply(lox,loy)
	z1 = karatsuba_multiply((lox+hix),(loy+hiy))
	z2 = karatsuba_multiply(hix,hiy)
	return (z2*10**(2*m2))+((z1-z2-z0)*10**m2)+(z0)


import time
import math
import random
#===================
# Problem 3-4d
#===================
# You may want to use this function to time the runtimes of 
# naive_multiply, karatsuba_multiply, and the native
# python multiply. The time module might be useful to you.

def time_functions():

    t_new=100
    for i in range(20)[:]:
        t_old=float(t_new)
    	print "n = "+str(2**i)
        import random
    	a=[str(random.randrange(0,10,1)) for i in range(2**i)]
        a=int(''.join(a))
        print "\n### SMART ###"
        t0=time.time()
        new=naive_multiply(a,a)
        #new=karatsuba_multiply(a,a)
        t1=time.time()
        t_new = t1-t0
        print "T(n): "+str(t_new)
        s=math.log(t_new/t_old,2)
        print "\nS = "+str(s)
        n=t_new/len(str(a))**s
        print "n = "+str(n)





time_functions()
