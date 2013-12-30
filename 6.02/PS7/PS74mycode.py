import sys, random
import wsim

class CWNode(wsim.Node):
    def __init__(self,location,network,retry):
        pass
    def channel_access(self,time,psize,nnodes):
        pass    
    def on_collision(self,packet):
        pass
    def on_xmit_success(self,packet):
        pass

class CWNet(wsim.Network):
    def __init__(self,wmin,wmax,simplecount,tsim,nnodes,psize,skew):
        self.wmin = wmin
        self.wmax = wmax
        self.simplecount = simplecount
        wsim.Network.__init__(self,tsim,nnodes,psize,skew)
    def make_node(self,loc,retry):
        return CWNode(loc,self,retry)

if __name__ == '__main__':
    narg = len(sys.argv)
    T = 10000
    if narg>1: T = int(sys.argv[1])
    N = 10
    if narg>2: N = int(sys.argv[2])
    P = 4
    if narg>3: P = int(sys.argv[3])
    pmin = 0.2
    if narg>4: wmin = int(sys.argv[4])
    pmax = 0.8
    if narg>5: wmax = int(sys.argv[5])
    simplecount = False
    if narg>6: simplecount = sys.argv[6]=='0'
    S = (narg>7)

    net=CWNet(wmin,wmax,simplecount,T,N,P,S)
    net.sim(50)
