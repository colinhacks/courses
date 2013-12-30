import sys, random
import wsim

class CSMANode(wsim.Node):
    def __init__(self,location,network,retry):
        pass
    def channel_access(self,time,psize,nnodes):
        pass
    def on_collision(self,packet):
        pass
    def on_xmit_success(self,packet):
        pass

class CSMANet(wsim.Network):
    def __init__(self,pmin,pmax,alpha,tsim,nnodes,psize,skew):
        self.pmin = pmin
        self.pmax = pmax
        self.alpha = alpha
        wsim.Network.__init__(self,tsim,nnodes,psize,skew)
    def make_node(self,loc,retry):
        return CSMANode(loc,self,retry)

if __name__ == '__main__':
    narg = len(sys.argv)
    T = 10000
    if narg>1: T = int(sys.argv[1])
    N = 10
    if narg>2: N = int(sys.argv[2])
    P = 4
    if narg>3: P = int(sys.argv[3])
    pmin = 0.2
    if narg>4: pmin = float(sys.argv[4])
    pmax = 0.8
    if narg>5: pmax = float(sys.argv[5])
    alpha = 0.5
    if narg>6: alpha = float(sys.argv[6])
    S = (narg>7)
 
    net=CSMANet(pmin,pmax,alpha,T,N,P,S)
    net.sim(50)
