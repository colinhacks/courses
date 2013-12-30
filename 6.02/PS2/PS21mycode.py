import numpy

def linear(A,msg):
    """
    encode 1/0 string of length kN into 1/0 string of length nN
    using linear block (n,k,d) code described by its k-by-m matrix A
    """
    k=len(A)
    codewords = [msg[k*i:k*i+k] for i in range(len(msg)/k)]
    
    print msg,"\n",codewords
    out = ''
    for word in codewords:
        print word
        bits = numpy.array([int(a) for a in word])
        print "A: ",A
        print "bits: ",bits
        out+=word+''.join([str(d%2) for d in bits.dot(A)])
    return out       



"""if __name__ == "__main__":
    import sys
    assert len(sys.argv)>2, '%d arguments supplied, 2 needed' %(len(sys.argv)-1)
    A = numpy.array(eval(sys.argv[1]))
    msg = sys.argv[2]
    print linear(A,msg)
"""
A= numpy.array([[1, 1, 0],
       [1, 0, 1],
       [0, 1, 1],
       [1, 1, 1]])
msg="010101011000"
out=linear(A, msg)



