# This solution template should be turned in through our submission site, at
# https://alg.csail.mit.edu

######################################################################################
### WARNING:                                                                       ###
### Be sure to write the Python code yourself!  We do run sophisticated automated  ###
### comparisons between each pair of programs turned in.  We are saddened and      ###
### troubled each year when a few studentsturn in nearly identical programs, and   ###
### we have to administer appropriate consequences.  It is better to turn in a     ###
### statement that you didn't have time to complete the assignment than to turn in ###
### the same code as someone else.                                                 ###
######################################################################################


####################
### Problem 4-4f ###
####################

######################################################################################
## N will be an integer, e.g. 4                                                     ##
## C will be a tuple of tuples rep'ing car locations, e.g. ((0,0),(0,3),(2,1),(3,2))##
## Returned result should be a list of tuples of tuples each rep'ing a move         ##
## e.g. [((0,3), (0,2)), ((3,2), (3,1)), ((3,1), (2,1)), ((0,2), (0,1)),            ##
##       ((0,1), (0,0)), ((0,0), (1,0)), ((1,0), (2,0)), ((2,0), (2,1))]            ##
######################################################################################


### Implement me! ###

def DemoDerby(N, B, C):

	def getChildren(state):
		moves=[]
		states=[]
		#print "state: ",state
		for i in range(len(state)):
			old=state[i]

			state = [a for a in state]
			for (x,y) in [(-1,0),(1,0),(0,1),(0,-1)]:
				newx=x+state[i][0]
				newy=state[i][1]+y
				if newx >= 0 and newy >= 0 and newx < N and newy < N:
					if (newx, newy) not in B:
							moves.append((state[i],(newx,newy)))
							state[i] = (newx,newy)
							states.append(tuple(set(state)))
							state[i]=old
		return zip(moves, states)

	level={C:0}
	parent={C:None}
	moves={C:None}
	i=1
	frontier = [(None,C)]
	while frontier:
		#print "frontier: ",frontier
		next=[]
		for (irrel,u) in frontier:
			for v in getChildren(u):
				if v[1] not in level:
					level[v[1]] = i
					parent[v]=(irrel,u)
					#print "parent[",v,"] = ",(irrel,u)
					moves[v]=v[1]
					next.append(v)
					if len(v[1])==1:
						path=[v[0]]
						print v[0]
						print path
						temp=parent[v]
						while temp[0] is not None:
							print "yay"
							path.append(temp[0])
							print temp[0]
							print path
							temp=parent[temp]
						path.reverse()
						return path
		frontier = next
		i+=1


N=2
B=()
C=((0, 0), (1, 1))


#a=getChildren(((0, 0),(0, 3),(2, 1),(3, 2)))
a=DemoDerby(N,B,C)
print a




