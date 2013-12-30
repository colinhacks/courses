import numpy
import math
def recover(A,msg):
    print "###############################\nMESSAGE: ",msg
    k=len(A)
    m=len(A[0])
    n=k+m
    indices={}
    check = True
    num = 1
    data_ct = 0
    parity_ct=0
    
    while check:
        log = math.log(num,2)
        if log - math.floor(log) == 0.0:
            parity_ct+=1
            indices['p'+str(parity_ct)]= (num,bin(num)[2:],parity_ct)
        else:
            data_ct +=1
            indices['d'+str(data_ct)] = (num,bin(num)[2:],data_ct)
            if data_ct == k:
                check=False    
        num+=1
    print indices
    """
    takes k-by-m ndarray A describing an (n,k,d) linear code with d>2
    and 0/1 string msg of length nN,
    returns 0/1 string of length kN, recovering 1 possible single errors
    in every n-bit word
    """
    
    print n
    codewords = [msg[n*i:n*i+n] for i in range(len(msg)/n)]
    print codewords
    codewords=[[int(c) for c in a] for a in codewords]

    H_inv = A.transpose()
    num = len(H_inv)
    print H_inv
    parity_check = numpy.concatenate((H_inv,numpy.identity(num)),axis=1)
    print parity_check
    checks=[]
    final=''
    for p in codewords:
        codeword = numpy.array([a for a in p])
        print "codeword: ",codeword
        test = parity_check.dot(codeword)
        for i in range(len(test)):
            test[i] = int(test[i])%2
        checks.append(test)
        print "test: ",test
        adders=[]
        binval = ''.join([str(int(a)) for a in test])
        print "binval: ",binval
        #val=int(''.join([str(int(a)) for a in test[::-1]]),2)
        for number in range(k+m):
            testing=''.join(str(int(a)) for a in parity_check[:,number])
            print "testing: ",testing
            if testing == binval:
                adders.append(1)
            else:
                adders.append(0)
        print "adders: ",adders
        print "cw: ",codeword
        final_sum = numpy.sum((numpy.array(adders),numpy.array(codeword)),axis=0)
        final+=''.join(str(int(a)%2) for a in final_sum[0:k])
        """
        print val
        
        for key in indices.keys():
            print indices[key][0]
            if indices[key][0]==val:
                print "FOUND!!"
                new=indices[key][-1]
                type=key[0]
                if type == 'p':
                    new+=k
                
                if p[new-1]==0:
                    p[new-1]=1
                else:
                    p[new-1]=0
        print "New:",p
        final+=''.join(str(a) for a in p[0:k])"""
        print "FINAL!\n",final
    return final
                    
msg='000110110'
A=numpy.array([[0,0]])
r=recover(A,msg)


