import sys
import wsim
import math

class TDMANode(wsim.Node):
    def channel_access(self,time,psize,nnodes):
        if int(math.floor((time)%(nnodes*psize))) == self.get_id():
            return True
        else:
            return False

class TDMANet(wsim.Network):
    def make_node(self,loc,retry):
        return TDMANode(loc,self,retry)

if __name__ == '__main__':
    narg = len(sys.argv)
    T = 10000
    if narg>1: T = int(sys.argv[1])
    N = 10
    if narg>2: N = int(sys.argv[2])
    P = 4
    if narg>3: P = int(sys.argv[3])
    S = (narg>4)
 
    net=TDMANet(T,N,P,S)
    net.sim(50)
