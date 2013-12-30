import sys
import numpy as np

def analyse(channel, T=50000, n=50, k=50):

    y = channel.sendreceive(np.zeros(T))
    (h,b) = np.histogram(y,bins=n)
    x=[(b[i]+b[i+1])/2 for i in range(len(b)-1)]
    r=sum([1.0*j[0]*j[1] for j in zip(h,[b[i+1]-b[i] for i in range(len(b)-1)] )])
    fx=[a/r for a in h]
    R = [1.0]+[((np.array((y[:-m]+y[m:])).var())/(2*y.var()))-1 for m in range(k)[1:]]
    x=np.array(x)
    fx=np.array(fx)
    R=np.array(R)
    return (np.array(x),np.array(fx),np.array(R))


    """
    (x,fx,R) = analyse(channel,T,n,k)
    inputs:
      channel: instance of a class with method senreceive
               (channel.sendreceive takes one-dimensional Numpy array,
               returns one-dimensional Numpy array at leastas long)
      T: int (T>n, T>k)
      n: int (n>0)
      k: int (k>0)
    outputs:
      x:  one-dimensional Numpy array of length n
      fx: one-dimensional Numpy array of length n (non-negative)
      R:  one-dimensional Numpy array of length k
    """
        

if __name__ == '__main__':
    import psaudio
    import matplotlib.pyplot as plt
    
    fs = 8000
    if len(sys.argv)>1:
        fs = int(sys.argv[1])
    T = 50000
    if len(sys.argv)>2:
        T = int(sys.argv[2])
    n = 100
    if len(sys.argv)>3:
        n = int(sys.argv[3])
    k = 100
    if len(sys.argv)>4:
        k = int(sys.argv[4])
    
    audio = psaudio.AudioChannel(fs)
    (x,fx,R) = analyse(audio,T,n,k)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(x,fx)
    plt.grid()
    plt.xlabel('Noise PDF')
    plt.subplot(212)
    plt.plot(R,'r.-')
    plt.grid()
    plt.xlabel('Noise auto-correlation')
    plt.show()

    
