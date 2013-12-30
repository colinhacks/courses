import sys
import math
import numpy as np

class BasebandChannel():
    
    def __init__( self, channel, T=8):
        self.channel = channel
        self.T = T
        """
        bbch = BasebandChannel(channel,T)
        inputs:
            channel: an instance of a class with method
                y = channel.sendreceive(x),
                    taking one-dimensional Numpy array x,
                    returning one-dimensional Numpy array y,
                    at least len(x) long
            T: int (T>0)
        the resulting instance bbch of BasebandChannel must have attributes
            bbch.channel = channel
            bbch.T = T
        """
        pass
            
    def modulate( self, bits ):
        """
        x = bbch.modulate(bits)
        input:
            bits: one-dimensional Numpy array with 0/1/ elements
        output:
            x: one-dimensional Numpy array bbch.T times longer than "bits"
        """
        x=np.array([bits[t/self.T]*np.sin(2*np.pi*t/self.T) for t in range(len(bits)*self.T)])
        return x

    def demodulate( self, y ):
        """
        soft_bits = bbch.demodulate(y)
        input:
             y: one-dimensional Numpy array, at least 2*bbch.T long
        output:
             soft_bits: one-dimensional Numpy array, at least
             len(y)/self.T-1 long
        """
        soft_bits=[(1./self.T)*sum([y[t]*np.sin(2.*np.pi*t/self.T) for t in range(n*self.T,n*self.T+self.T)]) for n in range(len(y)/self.T)]
        return np.array(soft_bits)
        

if __name__ == '__main__':
    import psaudio
    import matplotlib.pyplot as plt
    import PS42mycode

    T = 8
    if len(sys.argv)>1:
        T = int(sys.argv[1])
    fs = 8000
    channel = PS42mycode.AbstractChannel(0.1,np.array([3,-1,-1]),20*T,5*T)
    if len(sys.argv)>2:
        fs = int(sys.argv[2])
        channel = psaudio.AudioChannel(fs)
    
    bbch = BasebandChannel(channel,T)

    x=np.hstack((np.zeros(50),np.ones(50)))
    x[[20,40]]=1.0
    x[[60,80]]=0.0

    y = bbch.demodulate(bbch.channel.sendreceive(bbch.modulate(x)))
 
    plt.bar(xrange(len(y)),y)
    plt.grid()
    plt.show()
