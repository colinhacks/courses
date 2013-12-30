import sys
import math, cmath, random
import numpy as np

NFFT = 2**20
ff = np.linspace(0,1,NFFT)
def fft(y):
    Y = np.abs(np.fft.fft(y,2*NFFT)[:NFFT])
    return Y/Y.max()

def mix(signals, MAXDELAY = 100):
    L = max([len(signal) for signal in signals])+MAXDELAY+1
    x = np.zeros(L)
    for signal in signals:
        k = round(random.random()*MAXDELAY)
        x += np.hstack((np.zeros(k), signal, 
                        np.zeros(L-len(signal)-k)))
    return x

bark = [0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0]
class Communicator():  
    barker = np.array(bark)  
    zz = np.zeros(40)
    def __init__( self, T=8, M=1, L=10):
        import matplotlib.pyplot as plt
        self.T = T
        self.M = M
        self.L = L
        self.maxl = 2**L
        self.w = 2*math.pi/T
        vals=np.arange(-145,145)
        self.h = .02*2*.95*np.sinc(.02*vals)*np.cos(self.w*vals)
        wt = np.linspace(0,self.w*(T-1),T)
        self.sn = np.sin(wt).reshape(1,T)
        self.cs = np.cos(wt).reshape(1,T)

        
    def band(self, y):
        print y
        a = np.convolve(y,self.h)
        return a

class Sender(Communicator):
    def modulate(self, bits):
        return bits.repeat(self.M).reshape(self.M*len(bits),1).dot(self.sn).reshape(-1)
        
    def sendbits( self, bits ):
        N = len(bits)
        assert N < self.maxl, 'bitlength %d > %d too large'%(N,self.maxl-1)
        btl = np.array([int(x) for x in bin(N+self.maxl)[3:]])
        return self.modulate(np.hstack((self.zz,self.barker,
                                        btl,bits,self.zz)))
    def sendmsg(self, msg):
        bitstr = ''.join([bin(256+ord(x))[3:] for x in msg])
        return self.sendbits(np.array([int(x) for x in bitstr]))


class Receiver(Communicator):
    def tau(self, y):
        N = len(y)
        n = N/self.T
        a = y[:n*self.T].reshape(n,self.T).dot(self.cs.transpose()).sum()
        b = y[:n*self.T].reshape(n,self.T).dot(self.sn.transpose()).sum()
        return float((-cmath.phase(complex(b,a)))/self.w % self.T)
    def eye(self, y, k=3):
        N = len(y)
        tau = self.tau(y)
        TM = self.T*self.M
        sn = np.sin(np.linspace(-self.w*tau,self.w*(N-1-tau),N))
        v = np.convolve(y*sn,np.ones(TM))
        kTM = k*TM
        n = len(v)/kTM
        return (np.array(xrange(kTM)), v[:n*kTM].reshape(n,kTM).transpose())
        
    def threshold(self,u):
        ub = u[u>0.5*u.max()].mean()+0.01
        w = u[(u>-0.01)*(u<ub)].copy()
        w.sort()
        i = (w[1:]-w[:-1]).argmax()
        return 0.5*(w[i]+w[i+1])
        
    def demodulate( self, y ):
        N = len(y)
        tau = self.tau(y)
        TM = self.T*self.M
        sn = np.sin(np.linspace(-self.w*tau,self.w*(N-1-tau),N))
        v = np.convolve(y*sn,np.ones(TM))
        n=len(v)/TM
        V=v[:(n*TM)].reshape((n,TM))    
        q0=V.var(0).argmax()
        gamma=self.threshold(V[:,q0])
        self.gamma = gamma
        self.q0 = q0
        self.Vq0 = V[:,q0]
        return np.array(self.Vq0>gamma).astype(int)
        
    def preamble(self, u):
        pre = np.array([0,0,0,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0])
        result = np.convolve(2*pre-1,2*u-1)
        return np.argmax(result)-18
        
    def getbits(self, y):
        bits = self.demodulate(y)
        bts = bits[self.preamble(bits)+19:]
        N = int(''.join([str(x) for x in list(bts[:self.L])]), base=2)
        Nr = N+self.L
        n = len(bts)
        return bts[self.L:Nr]

    def getmsg(self, y):
        w = 2**np.array(xrange(8))[::-1].reshape(8,1)
        bits = self.getbits(y)
        n = len(bits)
        m = n/8
        return ''.join([chr(x) for x in bits[:8*m].reshape(m,8).dot(w)])
        

if __name__ == '__main__':
    import psaudio
    import matplotlib.pyplot as plt
    import PS42mycode

    narg = len(sys.argv)
    C = (0.1,[-1,-1,4,1,1])
    if narg > 1:
        C = eval(sys.argv[1])
    if type(C)==type(0):
        channel = psaudio.AudioChannel(C)
    else:
        channel = PS42mycode.AbstractChannel(C[0],np.array(C[1]),25,25)
    T = 44
    if narg > 2:
        T = eval(sys.argv[2])
    M = 4
    if narg > 3:
        M = eval(sys.argv[3])
    sender = Sender(T,M)
    receiver = Receiver(T,M)
    msg = "It is a truth universally acknowledged, that a single man in"
    if narg > 4:
        if len(sys.argv[4])>0:
            msg = sys.argv[4]

    if narg <6:
        x = sender.band(sender.sendmsg(msg))
        y = receiver.band(channel.sendreceive(x))
        rmsg = receiver.getmsg(y)
        print msg
        print rmsg
        ii,eye = receiver.eye(y)
        plt.figure(1)
        plt.subplot(211)
        plt.plot(ii,eye,'b',ii[[0,-1]],receiver.gamma*np.ones(2),'r',
                 ii[receiver.q0+M*T].repeat(2),
                 np.array([0,eye.reshape(-1).max()]),'r')
        plt.grid()
        plt.subplot(212)
        plt.plot(receiver.Vq0,'.',
                 np.array([0,len(receiver.Vq0)]),
                 receiver.gamma*np.ones(2),'r')
        plt.grid()
        plt.show()
        quit()
 
    T2 = 16
    if narg > 5:
        T2 = eval(sys.argv[5])
    M2 = 9
    if narg > 6:
        M2 = eval(sys.argv[6])
    sender2 = Sender(T2,M2)
    receiver2 = Receiver(T2,M2)
    msg2 = "Once upon a midnight dreary, while I pondered weak and weary,"
    if narg > 7:
        msg2 = sys.argv[7]

    x = sender.band(sender.sendmsg(msg))
    x2 = sender2.band(sender2.sendmsg(msg2))
    xmix = mix((x,x2))
    ymix = channel.sendreceive(xmix)
    y = receiver.band(ymix)
    y2 = receiver2.band(ymix)
    
    rmsg = receiver.getmsg(y)
    rmsg2 = receiver2.getmsg(y2)

    print msg
    print rmsg
    print msg2
    print rmsg2
    
    ii,eye = receiver.eye(y)
    ii2,eye2 = receiver2.eye(y2)
    H = fft(sender.h)
    H2 = fft(sender2.h)
    X = fft(xmix)
    Y = fft(ymix)
    b = (ff<0.2)

    plt.figure(1)
    plt.subplot(321)
    plt.plot(ii,eye,'b',ii[[0,-1]],receiver.gamma*np.ones(2),'r',
             ii[receiver.q0+M*T].repeat(2),
             np.array([0,eye.reshape(-1).max()]),'r')
    plt.grid()
    plt.subplot(323)
    plt.plot(receiver.Vq0,'.',
             np.array([0,len(receiver.Vq0)]),
             receiver.gamma*np.ones(2),'r')
    plt.grid()
    plt.subplot(325)
    plt.plot(ff[b],X[b],'b',ff[b],H[b],'r',ff[b],H2[b],'g')
    plt.grid()
    plt.subplot(322)
    plt.plot(ii2,eye2,'b',ii2[[0,-1]],receiver2.gamma*np.ones(2),'r',
             ii2[receiver2.q0+M2*T2].repeat(2),
             np.array([0,eye2.reshape(-1).max()]),'r')
    plt.grid()
    plt.subplot(324)
    plt.plot(receiver2.Vq0,'.',
             np.array([0,len(receiver2.Vq0)]),
             receiver2.gamma*np.ones(2),'r')
    plt.grid()
    plt.subplot(326)
    plt.plot(ff[b],Y[b],'b',ff[b],H[b],'r',ff[b],H2[b],'g')
    plt.grid()
    
    plt.show()
    


[0,0,0,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0]