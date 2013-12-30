import sys
import math, cmath, random
import numpy as np


class Communicator():
    
    def __init__( self, T=8, M=1):
        self.T = T
        self.M = M

        

class Sender(Communicator):

    def modulate(self, bits):
        out=[]
        for t in range(len(bits)*self.M*self.T):
            n=t/(self.M*self.T)
            om=2*math.pi/self.T
            out.append(bits[n]*math.sin(om*t))
        return np.array(out)
    

class Receiver(Communicator):

    def tau(self, y):
        print "T: ",self.T
        omega=(2*math.pi/self.T)
        a=0
        b=0
        for t in range(len(y)):
            a+=y[t]*math.cos(2*t*math.pi/self.T)
            b+=y[t]*math.sin(2*t*math.pi/self.T)
        alpha = a/math.sqrt(a**2 + b**2)
        beta = b/math.sqrt(a**2 + b**2)
        exp = complex(beta,(-1)*alpha)
        print exp
        phase = cmath.phase(exp)
        ans=phase/omega
        while ans<0:
            print ans
            ans+=self.T
        
        #print "ans ",ans
        return ans

    def eye(self, y):
        print "Tests"
        print "T: ",self.T
        print "len(y): ",len(y)
        print "max i: ",len(y)+self.T*self.M-2
        print "max t: ",
        
        # def get(key):
        #     if key<0 or key>=len(y):
        #         return 0
        #     else:
        #         return y[key]*math.sin((2*math.pi/self.T)*(key-tau))

        
        tau=self.tau(y)
        irange=3*self.M*self.T
        krange=(len(y)+self.M*self.T-1)/(3*self.M*self.T)
        v=[0.0]*(irange*krange)
        for i in range(irange*krange):#3*self.M*self.T):
            val=0.0
            for key in range(i-self.M*self.T+1,i+1):
                if key>=0 and key<len(y):
                    val+=y[key]*math.sin((2*math.pi/self.T)*(key-tau))
                    #v[key]=sum([y[key]*math.sin((2*math.pi/self.T)*(key-tau)) for t in range(i-self.M*self.T+1,i+1)])
            v[i]=val
        print "len V:",len(v)
        print "Theoretical len v: ",len(y)+self.T*self.M-1
        print 1.*(len(y)+self.T*self.M-1)/(3*self.M*self.T)
        var=3*self.M*self.T
        a= np.array(v).reshape((len(y)+self.M*self.T-1)/(3*self.M*self.T),3*self.M*self.T)
        a=np.transpose(a)
        print "len a: ",len(a)
        print ((len(y)+self.M*self.T-1)/(3*self.M*self.T))*(3*self.M*self.T)
        return (np.array(xrange(3*self.M*self.T)),a)            

if __name__ == '__main__':
    import psaudio
    import pyaudio
    import matplotlib.pyplot as plt
    import PS42mycode

    p = pyaudio.PyAudio()
    print(p.get_device_info_by_index(2))

    T = 8
    if len(sys.argv)>1:
        T = int(sys.argv[1])
    M = 1
    if len(sys.argv)>2:
        M = int(sys.argv[2])
    C = [-1,-1,4,1,1]
    if len(sys.argv)>3:
        C = eval(sys.argv[3])
    if type(C)==type(0):
        channel = psaudio.AudioChannel(C)
    else:
        channel = PS42mycode.AbstractChannel(C[0],np.array(C[1]),5*M*T,25)

    bts = np.array([random.choice((0,1)) for i in xrange(500)])
    bits = np.hstack((np.zeros(20),bts,np.zeros(20)))
    sender = Sender(T,M)
    receiver = Receiver(T,M)
    x = sender.modulate(bits)
    y = channel.sendreceive(x)
    tau = receiver.tau(y)
    ii,eye = receiver.eye(y)
   
    t = np.array(xrange(len(y)))
    v = np.sin((2*math.pi/sender.T)*(t-tau))*y
    
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t,v)
    plt.grid()
    plt.subplot(212)
    plt.plot(ii, eye)
    plt.grid()
    plt.show()
