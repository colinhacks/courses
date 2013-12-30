import random,sys,math
import netsim


# your router class
class DVRouter(netsim.Router):
    def make_advertisement(self):
        return [(addr,self.spcost[addr]) for addr in self.routes.keys()]
    
    def link_failed(self, link):
        for (addr, route) in self.routes.items():
            if self.routes[addr] = link:
                del spcost[addr]
                del routes[addr]

        
    def integrate_advertisement(self, adv, link, time):
        w = link.cost
        newsp={}
        for (node,dist) in adv:
            real=w+dist
            if real<self.spcost[node]:
                newsp[node] = real
            elif real>self.spcost[node] and self.routes[node] == link
                newsp[node]=real
        spcost=newsp

        

class DVRouterNetwork(netsim.RouterNetwork):
    def make_node(self,loc,address=None):
        return DVRouter(loc,address=address)


if __name__ == '__main__':
    narg = len(sys.argv)
    N = 0
    if narg>1: N = int(sys.argv[1])

    if N>1:
        rg = netsim.RandomGraph(N)
        (NODES, LINKS) = rg.genGraph()
    elif N==1:
        NODES = (('A',0,0),('B',0,1),('C',1,0))
        LINKS = (('A','B'),('A','C'))
    elif N==0:
        NODES = (('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),)
        LINKS = (('A','B'),('B','C'),('C','D'),)
    else:
        #   A---B   C---D
        #   |   | / | / |
        #   E   F---G---H
        # format: (name of node, x coord, y coord
        NODES =(('AA',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
                ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1))

        # format: (link start, link end)
        LINKS = (('AA','B'),('AA','E'),('B','F'),('E','F'),
                 ('C','D'),('C','F'),('C','G'),
                 ('D','G'),('D','H'),('F','G'),('G','H'))

    net = DVRouterNetwork(10000, NODES, LINKS, 0)
    sim = netsim.NetSim()
    sim.SetNetwork(net)
    sim.MainLoop()

 
        

