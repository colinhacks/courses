import sys
import numpy as np

class AbstractChannel():
    def __init__(self, sigma=0.001, usr=np.array([3,-1,-1]), lag=50, pad=30):
        """
        ch = AbstractChannel(sigma,usr,lag,pad)
        inputs:
            sigma: float (sgma>0)
            usr: one-dimensional Numpy array
            lag: int (lag>0)
            pad: int (pad>0)
        """
        self.sigma = sigma
        self.usr = usr
        self.lag = lag
        self.pad = pad
    
    def sendreceive( self, x ):
        """
        y = ch.sendreceive(x)
        input:
            x: one-dimansional Numpy array
        output:
            y: one-dimensional Numpy array
        """       
        
        conv=np.convolve(self.usr,x)
        conv=[self.sigma*np.random.randn()+val for val in conv]
        a=np.array([b for b in np.zeros(self.lag)]+[c for c in np.array(conv)]+[d for d in np.zeros(self.pad)])
        return a

if __name__ == '__main__':

    import PS41mycode
    import matplotlib.pyplot as plt
    import psaudio
    print "PLOTTING!"
    sigma = 0.001
    if len(sys.argv)>1:
        sigma = float(sys.argv[1])
    fs = 8000
    if len(sys.argv)>2:
        fs = int(sys.argv[2])

    audio = psaudio.AudioChannel(fs)
    abstr = AbstractChannel(sigma)
    (xau,fau,Rau) = PS41mycode.analyse(audio)
    (xab,fab,Rab) = PS41mycode.analyse(abstr)
    m = len(Rau)
    
    plt.figure(1)
    plt.subplot(211)
    plt.plot(xau,fau,'b',xab,fab,'r')
    plt.grid()
    plt.xlabel('Noise PDF: sigma=%f'%sigma)
    plt.subplot(212)
    plt.plot(xrange(m),Rau,'b.-',xrange(m),Rab,'r.-')
    plt.grid()
    plt.xlabel('Noise auto-correlation')
    plt.show()
