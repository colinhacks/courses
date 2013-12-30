def optimal(k):
    import math,numpy
    print "k: ",k
    """
    output k-by-m ndarray
    representing the A matrix of a linear (n,k,3) code
    with minimal possible n
    """
    indices={}
    check = True
    num = 1
    data_ct = 0
    parity_ct=0
    
    while check:
        log = math.log(num,2)
        if log - math.floor(log) == 0.0:
            parity_ct+=1
            indices['p'+str(parity_ct)]= (num,bin(num)[2:])
        else:
            data_ct +=1
            indices['d'+str(data_ct)] = (num,bin(num)[2:])
            if data_ct == k:
                check=False    
        num+=1
    #print indices
    A=[]
    """
    for i in range(k+1)[1:]:
        print "i: ",i
        A.append([(lambda a,b: 0 if '0' not in bin(indices['d'+str(a)][0]+indices['p'+str(b)][0])[2:] else 1)(i,x) for x in range(parity_ct+1)[1:]])                    
        print A,"\n\n"

    """
    for i in range(k+1)[1:]:
        #print "#######################\ni: ",i
        string=[]
        #print range(parity_ct+1)[1:]
        for x in range(parity_ct+1)[1:]:
            
            #print "x: ",x
            data = indices['d'+str(i)][0]
            parity = indices['p'+str(x)][0]
            #print "data: ",data
            #print "parity: ",parity
            realbinary=bin(data)[2:]
            realbinary=''+realbinary
            #print "realbinaryhhh: ",realbinary
            #print "-x: ",-x
            binary=bin(indices['d'+str(i)][0]+indices['p'+str(x)][0])[2:]
            #print "Binary: ",binary
            if len(realbinary)<x or realbinary[-x]=='0':#'0' not in binary:
                string.append(0)
                #print "#######\nd"+str(i)+" not in i"+str(x)+"\n##########"
            else:
                 string.append(1)
            #print "string is now: ",string
            #print "END INNER"
        A.append(string)
        #print "appended to A: ",string
    
    return numpy.array(A)
    

A = optimal(4)

