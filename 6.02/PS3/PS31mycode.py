import sys
import numpy

def conv(W,u):
    W=numpy.array([numpy.array(a) for a in W])
    """
    y = conv(W,u)
    W: r-by-K 0/1 numpy array 0/1 (for convolution code )
    u: 0/1 numpy vector of length T (binary input to be encoded)
    y: 0/1 numpy vector of length T*r (convolutional encoding of u)
    """
    K=len(W[0])
    r=len(W)
    window=numpy.array([0]*K)
    code=[]
    for char in u:
        window=numpy.insert(window[:-1], 0,[char])
        for eqn in W:
            code.append(eqn.dot(window)%2)
    return numpy.array(code)
    

if __name__ == "__main__":
    if len(sys.argv)>2:
        W = numpy.array(eval(sys.argv[1]))
        u = numpy.array([int(x) for x in sys.argv[2]])
        print ''.join([str(int(x)) for x in conv(W,u)])


print conv(numpy.array([[1,1,0],[1,1,1]]), [int(a) for a in '0100110001001011010101'])
