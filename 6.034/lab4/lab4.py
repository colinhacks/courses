from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    var = state.get_current_variable()
    value=None
    if var is not None:
        value = var.get_assigned_value()
        constraints = state.get_constraints_by_name(var.get_name())
        while constraints:
            con = constraints.pop()
            if con.get_variable_i_name() == var.get_name():
                active=con.get_variable_j_name()
            else:
                active=con.get_variable_i_name()
            j=state.get_variable_by_name(active)

            for jval in j.get_domain():

                a=con.check(state,value_i=value,value_j=jval)


                if not a:
                    j.reduce_domain(jval)
                    
                if j.domain_size() == 0:
                    #print "\n------------\nTEST FAILS\n------------"
                    return False
        return True
    return True

    

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    queue = set([a for a in state.get_all_variables() if a.domain_size()==1])
    visited=set()
    
    while queue:
        new=queue.pop()
        value = new.get_domain()[0]
        visited.add(new)
        constraints = state.get_constraints_by_name(new.get_name())
        
        while constraints:
            con = constraints.pop()
            if con.get_variable_i_name() == new.get_name():
                active=con.get_variable_j_name()
            else:
                active=con.get_variable_i_name()
            j=state.get_variable_by_name(active)
            for jval in j.get_domain():
                if not con.check(state,value_i=value,value_j=jval):
                    j.reduce_domain(jval)
                if j.domain_size() == 0:
                    return False
        queue = set([a for a in state.get_all_variables() if a.domain_size()==1])-visited
    return True


## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
#print senate_people
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    #print list1
    #print list2
    return sum([1.*(list1[a]-list2[a])**2 for a in range(len(list1))])**(1./2)
    # this is not the right solution!
    #return hamming_distance(list1, list2)

#Once you have implemented euclidean_distance, you can check the results:
#print evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2)

#print evaluate(nearest_neighbors(euclidean_distance, 3), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 3)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    totals = len(yes)+len(no)
    yesdem=len([a for a in yes if a=="Democrat"])
    yesrep=len([a for a in yes if a=="Republican"])
    nodem=len([a for a in no if a=="Democrat"])
    norep=len([a for a in no if a=="Republican"])
    in1=1.*yesdem/len(yes)
    in2=1-in1
    in3=1.*nodem/len(no)
    in4=1-in3
    a1=[a for a in [in1,in2] if a != 0.]
    a2=[a for a in [in3,in4] if a != 0]
    info1 = -1*sum([a*math.log(a,2) for a in a1])
    d1=1.0*len(yes)/totals
    info2 = -1*sum([a*math.log(a,2) for a in a2])
    d2=1.0*len(no)/totals
    return info1*d1+info2*d2
    #return homogeneous_disorder(yes, no)

#print CongressIDTree(senate_people, senate_votes, information_disorder)
evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)
#
## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 44
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
## Now, find a value of n that classifies at least 95 of last year's senators correctly.

N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
print old_senator_classified

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "3"
WHAT_I_FOUND_INTERESTING = "Seeing the drastic change in the amount of data required to classify the senate between the 109th and 110th congress.  What a great problem."
WHAT_I_FOUND_BORING = "n/a"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
