from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

#Add back in variables
def backchain_to_goal_tree(rules, hypothesis):
    #print "Rules: ",rules
    print "H: ",hypothesis
    #if hypothesis=='zot':
    #print "Rules: ",rules
    #nodes=[rule.antecedent() for rule in rules if (match(rule.consequent()[0],hypothesis) or match=={})]
    #print nodes
    a={}
    nodes=[]
    for rule in rules:
        #print "Consequent: ",rule.consequent()[0]
        d=match(rule.consequent()[0],hypothesis)
        #print d
        if d or d=={}:
            #print "MATCHED!!"
            nodes.append(rule.antecedent())
            #print rule.antecedent()
            #print nodes
        test_match=match(rule.consequent()[0],hypothesis)
        if test_match:
            a = dict(a.items()+test_match.items())
    print a
    
    tree=OR(hypothesis)
    
    for node in nodes:
        print "type: ",type(node)
        if type(node) is OR or type(node) is AND:
            print "\n\nAppending list of nodes: ",[backchain_to_goal_tree(rules, populate(elem,a)) for elem in node]
            tree.append(type(node)([backchain_to_goal_tree(rules, populate(elem,a)) for elem in node]))
        else:
            print "\n\nAppending node: ",backchain_to_goal_tree(rules,populate(node,a))
            
            tree.append(backchain_to_goal_tree(rules,populate(node,a)))
    print "\n\n#####TREE!!\n",simplify(tree)
    
                
    
    return simplify(tree)
# Here's an example of running the backward chainer - uncomment
# it to see it work:
a= backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
print a
