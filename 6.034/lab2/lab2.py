# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    agenda=[[start]]
    while agenda:

        expand=agenda.pop(0)
        if expand[-1]==goal:
            return expand
        agenda+=[expand+[a] for a in graph.get_connected_nodes(expand[-1]) if a not in expand]
        
        #print agenda
        
    
    
    

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    agenda=[[start]]
    while agenda:

        expand=agenda.pop(0)
        if expand[-1]==goal:
            return expand
        agenda=[expand+[a] for a in graph.get_connected_nodes(expand[-1]) if a not in expand]+agenda


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    agenda=[[start]]
    while agenda:

        expand=agenda.pop(0)
        if expand[-1]==goal:
            return expand
        agenda=sorted([expand+[a] for a in graph.get_connected_nodes(expand[-1]) if a not in expand],key=lambda x:graph.get_heuristic(x[-1],goal))+agenda
    

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    #print "GOAL: ",goal
    agenda1=[[start]]
    agenda2=[]
    while True:
        while agenda1:
            #print "AGENDA 1: ",agenda1
            expand=agenda1.pop(0)
            if expand[-1]==goal:
                return expand
            agenda2+=[expand+[a] for a in graph.get_connected_nodes(expand[-1]) if a not in expand]
        agenda2=sorted(agenda2,key=lambda x:graph.get_heuristic(x[-1],goal))[:beam_width]
        agenda1=agenda2
        agenda2=[]
        """
        #print "SORTED AND TRIMMED ONE: ",agenda2
        while agenda2:
             #print "AGENDA 2: ",agenda2
             expand=agenda2.pop(0)
             if expand[-1]==goal:
                 return expand
             agenda1+=[expand+[a] for a in graph.get_connected_nodes(expand[-1]) if a not in expand]
        agenda1=sorted(agenda1,key=lambda x:graph.get_heuristic(x[-1],goal))[:beam_width]
        #print "SORTED AND TRIMMED TWO : ",agenda2
        """
        if not agenda1 and not agenda2:
            return []
                
        
## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    return sum([graph.get_edge(a,b).length for (a,b) in zip(node_names,node_names[1:])])


def branch_and_bound(graph, start, goal):
    cost=lambda x:path_length(graph,x)#+graph.get_heuristic(x[-1],goal)
    agenda=[[start]]
    if start==goal:
        return []
    best=None
    while agenda:
        #print "LENGTH OF AGENDA: ",len(agenda)
        #print []
        expand=agenda.pop(0)
        for a in graph.get_connected_nodes(expand[-1]):
            heuristic_cost=cost(expand+[a])
            actual_cost=path_length(graph,expand+[a])
            if a == goal and ((not best) or actual_cost<best[1]):
                best = (expand+[a],actual_cost)
                #print "NEW BEST:",actual_cost
            if a not in expand:
                agenda=[expand+[a]]+agenda
            #agenda=[expand+[a] for a in graph.get_connected_nodes(expand[-1]) if a not in expand and ((not best) or actual_cost<best[1])]+agenda
            agenda=sorted(agenda,key=cost)
            #print agenda
        #print [cost(a) for a in agenda]
    if best:
        return best[0]
    else:
        return []

def a_star(graph, start, goal,bt=False):
    if not bt:
        print "THE GOAL IS: ", goal
        cost=lambda x:path_length(graph,x)+graph.get_heuristic(x[-1],goal)
        agenda=[[start]]
        
        best=None
        extended={}
        while agenda:
            #print "################"
            #print "##  Len: ",len(agenda),"     ###"
            #print "##############"
            #print "LENGTH OF AGENDA: ",len(agenda)
            #print []
            expand=agenda.pop(0)
            actual_cost=path_length(graph,expand)
            #if expand == [start]:
                #print "ORIG: ",actual_cost
            if expand[-1] is goal:
                print "FOUND  A PATH!!"
                return expand
            if expand[-1] in extended:# and extended[expand[-1]][0]<=actual_cost:
                asdfsdf=1
                print 'extended already'
            
            else:
                #print "EXPANDING ",expand[-1]
                extended[expand[-1]]=(actual_cost,expand)
                #print extended
                for a in graph.get_connected_nodes(expand[-1]):
                    #print "Comparing: ",a,goal
                    actual_cost=path_length(graph,expand+[a])
                    if a not in expand:
                        #print "ADDED TO AGENDA: ",expand+[a]
                        heuristic_cost=cost(expand+[a])
                        actual_cost=path_length(graph,expand+[a])
                        agenda=[expand+[a]]+agenda
                        agenda=sorted(agenda,key=cost)
                    #else:
                        #print "LOOPING PATH.\n"
                    if a == goal:
                        #print "FOUND GOAL"
                        extended[goal]=(actual_cost,expand+[a])
                        agenda=[b for b in agenda if cost(b)<=actual_cost]
                        #print agenda
                    #print "costs: ",[path_length(graph,b) for b in agenda]
                #print [cost(a) for a in agenda]
            #print agenda
        if goal in extended:
            return extended[goal][1]
        else:
            return []
    else:
        print "THE GOAL IS: ", goal
        cost=lambda x:path_length(graph,x)+graph.get_heuristic(x[-1],goal)
        agenda=[[start]]
        
        best=None
        extended={}
        while agenda:
            #print "################"
            #print "##  Len: ",len(agenda),"     ###"
            #print "##############"
            #print "LENGTH OF AGENDA: ",len(agenda)
            #print []
            expand=agenda.pop(0)
            actual_cost=path_length(graph,expand)
            #if expand == [start]:
                #print "ORIG: ",actual_cost
            if expand[-1] in extended and extended[expand[-1]][0]<=actual_cost:
                asdfsdf=1
                print 'extended already'
            
            else:
                #print "EXPANDING ",expand[-1]
                extended[expand[-1]]=(actual_cost,expand)
                #print extended
                for a in graph.get_connected_nodes(expand[-1]):
                    #print "Comparing: ",a,goal
                    actual_cost=path_length(graph,expand+[a])
                    if a not in expand:
                        #print "ADDED TO AGENDA: ",expand+[a]
                        heuristic_cost=cost(expand+[a])
                        actual_cost=path_length(graph,expand+[a])
                        agenda=[expand+[a]]+agenda
                        agenda=sorted(agenda,key=cost)
                    #else:
                        #print "LOOPING PATH.\n"
                    if a == goal:
                        #print "FOUND GOAL"
                        extended[goal]=(actual_cost,expand+[a])
                        agenda=[b for b in agenda if cost(b)<=actual_cost]
                        #print agenda
                    #print "costs: ",[path_length(graph,b) for b in agenda]
                #print [cost(a) for a in agenda]
            #print agenda
        if goal in extended:
            return extended[goal][1]
        else:
            return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        print "path length: ",path_length(graph, branch_and_bound(graph,node,goal))
        print "heuristic: ",graph.get_heuristic(node, goal)
        if path_length(graph, branch_and_bound(graph,node,goal))<graph.get_heuristic(node, goal):
            return False
    return True

def is_consistent(graph, goal):
    if not is_admissible(graph,goal):
        return False
    for edge in graph.edges:
        if graph.get_heuristic(edge.node1,goal)>edge.length+graph.get_heuristic(edge.node2,goal):
            return False
        if graph.get_heuristic(edge.node2,goal)>edge.length+graph.get_heuristic(edge.node1,goal):
            return False
    if graph.get_heuristic(goal,goal) !=0:
        return False
    return True

    """distances=[]
    for node in graph.nodes:
        distances.append((node,path_length(graph, a_star(graph,node,goal))))
    distances=sorted(distances,key=lambda x:-1*x[1])
    heuristic=None
    for node in graph.nodes:
        for a in graph.get_connected_nodes(node):
            if distances[a]<distances[node]:
                if graph.get_heuristic(a,goal)>graph.get_heuristic(node,goal):
                    return False
            else:
                if graph.get_heuristic(a,goal)<graph.get_heuristic(node,goal):
                    return False"""
        
        
        
    
        



HOW_MANY_HOURS_THIS_PSET_TOOK = '6'
WHAT_I_FOUND_INTERESTING = 'most of it'
WHAT_I_FOUND_BORING = 'Debugging for hours after I included backtracking in my a-star search and it got the wrong answer on the last test for a long time. Include a note in the pset maybe?'

