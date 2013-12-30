def huffman(pList):
    original = pList
    """
    argument: pList -- numpy.array of probabilities
    return: (codeBook, codeLength)
       codeBook   -- a Huffman code: codeBook[k] encodes the symbol
                     with probability pList[k]
    codeLength -- code length for the codeBook
    """
    # GENERIC PROBABILITY CLASS
    class Prob:
        def __init__(self,prob,index):
            self.prob = prob
            self.index = index
            
        def __str__(self):
            return "Prob: "+str(self.prob)
    #PROB SUBCLASS FOR LEAVES OF TREE (codewords)
    class Node(Prob):
        
        def __init__(self,prob,left, right):
            self.prob = prob
            self.left=left
            self.right=right
    #GENERIC NODE (binary node with two branches
    class Leaf(Prob):
        def __init__(self, index,prob, prefix='',parent=None):
            self.prob = prob
            self.prefix = prefix
            self.parent = parent
            self.index=index
    # Takes Node and appends prefix '0' to all prefixes of Leaves in left, and vice versa      
    def add_prefix(self, prefix):
        #Add prefix to all leaf children of a node
        if isinstance(self, Node):
            add_prefix(self.left,prefix)
            add_prefix(self.right,prefix)
        if isinstance(self, Leaf):
            print "Leaf with prob ",self.prob," changed from ",self.prefix,"\nto ",prefix+self.prefix
            self.prefix = prefix+self.prefix
            
    reals=pList
    pList=[]
    for i in range(len(reals)):
        if True:#reals[i]:
            pList.append(Leaf(i,reals[i]))
    pList = sorted(pList,key=lambda x: x.prob)

    print [a.prob for a in pList],"\nSORTED!"


    
    
    while len(pList)>1:
        add_prefix(pList[0],'0')
        add_prefix(pList[1],'1')
        low1=pList[0]
        low2=pList[1]

        node = Node(low1.prob+low2.prob, low1, low2)
        low1.parent = node
        low2.parent = node
        pList = sorted(pList[2:]+[node],key=lambda x: x.prob)
        print "Loop Success"
        print [(a.prob) for a in pList],"\nSORTED!"
        
    def unpack(node):
        if isinstance(node.left, Node):
            a = unpack(node.left)
        if isinstance(node.left, Leaf):
            a= [node.left]
        if isinstance(node.right, Node):
            b = unpack(node.right)
        if isinstance(node.right, Leaf):
            b= [node.right]
        return a+b
    
    list_of_leaves = unpack(pList[0])
    leaves = {}
    for leaf in list_of_leaves:
        leaves[leaf.index]=(leaf.prefix,leaf.prob)
        print "Entered: {",leaf.index," : (",leaf.prefix,", ",leaf.prob,") }"

    codes = []
    probs = []
    for i in sorted(leaves.iterkeys()):
        print "i: " ,i
        codes.append(leaves[i][0])
        probs.append(leaves[i][1])
        print "Codebook entry: ",leaves[i]

    length=0
    for i in range(len(codes)):
        length+=probs[i]*len(codes[i])
    print "################\ncodes: ",codes
    print "\n################\nlength: ",length
    return (codes, length)
        
        
 
if __name__ == "__main__":
    import sys
    import numpy
    import PS1bin
    if len(sys.argv)>1:
        pList = numpy.array(eval(sys.argv[1]))
    else:
        pList = PS1bin.get_dist(5)
    print 'pList = ', pList
    (codeBook, codeLength) = huffman(pList)
    print 'codeLength = ', codeLength
    print 'codeBook:'
    for x in codeBook:
        print x



