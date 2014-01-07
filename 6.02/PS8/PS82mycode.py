import random,sys,math
import netsim

def dijkstra(src, LSAd):
    parents={}
    print "LSAd: ",LSAd
    routes={}
    visited=set()
    dist={src:0}
    heap = [(src,0)]
    while heap:
        print "HEAP: ",heap
        heap = sorted(heap,key=lambda x:x[1])
        next=heap.pop(0)[0]

        if next not in visited:
            visited.add(next)
            print "next"
            print next
            print LSAd[next]
            for (node,distance) in LSAd[next]:
                
                if node not in visited:
                    heap.append((node,distance))
                    parents[node]=next
                    dist[node]=dist[next]+distance

    print "parents: ",parents
    for node in dist.keys():
        if node!=src:
            active=node
            path=[node]
            while active != src:
                path.insert(0,parents[active])
                active=parents[active]
            print path
            routes[node]=path[1]
    routes[src]=src
    return (dist,routes)

    
    

class LSRouter(netsim.Router):
    INFINITY = sys.maxint

    def __init__(self,location,address=None):
        netsim.Router.__init__(self, location, address=address)
        self.LSAd = {}      # addr -> [(nbr1,cost1),(nbr2,cost2),...]
        self.LSAt = {}      # addr -> (expiration, seq)
        self.seq = 0        # uniquely identify each LSA broadcast
        self.queue = [None] # advertisement (addr, seq, data) queue

    def make_advertisement(self):
        for addr in self.LSAt.keys():       # remove stale LSAs
            if self.seq > self.LSAt[addr][0]:
                del self.LSAt[addr]
                del self.LSAd[addr]
        adv = self.queue.pop()              # adv to send
        if adv == None:                     # prepare own adv
            self.seq += 1
            self.queue.insert(0,None)
            adv = (self.address, self.seq, self.construct_lsa())
        return adv

    def construct_lsa(self):
        return [(nghbr, lcost) for tst, nghbr, lcost in self.neighbors.values()]

    def accept_adv_as_new(self,adv):
        self.LSAt[adv[0]] = (self.seq+10, adv[1])
        self.LSAd[adv[0]] = adv[2]
        self.queue.insert(0,adv)
    
    def integrate_advertisement(self, adv, link, time):
        self.LSAd[self.address] = self.construct_lsa()
        self.LSAt[self.address] = (self.seq+10, self.seq)
        if adv[0] not in self.LSAt:
            self.accept_adv_as_new(adv)
        elif adv[1] > self.LSAt[adv[0]][1]:
            self.accept_adv_as_new(adv)
        self.spcost, rt = dijkstra(self.address, self.LSAd)
        self.routes = dict([(addr, self.getlink(rt[addr])) for addr in rt])

    def OnClick(self,which):
        if which == 'left':
            print self
            print '  LSAd:'
            for (key,value) in self.LSAd.items():
                print '    ',key,': ',value
        netsim.Router.OnClick(self,which)

# A network with nodes of type LSRouter
class LSRouterNetwork(netsim.RouterNetwork):
    def make_node(self,loc,address=None):
        return LSRouter(loc,address=address)


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

    net = LSRouterNetwork(10000, NODES, LINKS, 0)
    # setup graphical simulation interface
    
    sim = netsim.NetSim()
    sim.SetNetwork(net)
    sim.MainLoop()
    
 

