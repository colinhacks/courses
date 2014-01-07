import random,sys,math
import netsim


# your router class
class DVRouter(netsim.Router):
    def make_advertisement(self):
        print "-------------\nCREATING AD FOR ",self.address
        print "neighbors"
        print self.neighbors
        print "routes"
        print self.routes
        print "spcost"
        print self.spcost
        a= [(addr,self.spcost[addr]) for addr in self.spcost.keys() if self.spcost[addr]<self.INFINITY]
        #print a
        print self.neighbors
        for (timestamp, address, linkcost) in self.neighbors.values():
            print "address",address
            print a
            if (address not in [b[0] for b in a]) or linkcost<self.spcost[address]:#a.append((address,linkcost))
                a.append((address,linkcost))
        print "Advertisement:",a
        return a
    
    def link_failed(self, link):
        print self.address,self.neighbors
        print "\nLINK FAILED TRIPPED\n"
        for (addr, route) in self.routes.items():
            if self.routes[addr] == link:
                if link in self.neighbors:
                    del self.neighbors[link]
                del self.spcost[addr]
                del self.routes[addr]

        
    def integrate_advertisement(self, adv, link, time):
        print "\n#########################"
        print "##  Integrate Advert  ###"
        print "#########################"
        print "Link: ",link
        w=link.cost
        newsp={self.address:0}
        newroutes={self.address:'Self'}
        # Potential destinations
        dests=[a[0] for a in adv]
        print "Dests ",self.address,dests
        for (node,dist) in adv:

            print "\n### New dist-node pair  ####\nlooking at: ",self.address
            print "(Node, dist):",(node,dist)

            real=w+dist    
            if node not in self.spcost.keys() or real<self.spcost[node]:
                print self.address," -> ",node," has new cost ",real
                newsp[node] = real
                newroutes[node]=link
            elif real>self.spcost[node] and self.routes[node] == link:
                print self.address," -> ",node," has bigger cost ",real
                newsp[node]=real
                newroutes[node]=link
            else:
                print "no update"
            print "\n"




            # Check time
            if (node in self.last.keys()) and (time==self.last[node]):
                update=True
                self.dests[node]=[]
            else:
                update=False
            
        
        for (key,(a,b,c)) in self.neighbors.items():
            if b not in newsp.keys() or c<newsp[b]:
                if key.broken==False:
                    newsp[b]=c
                    newroutes[b]=key
        print "NEW SP !!!",dict(self.spcost,**newsp)

        # Setting spcost and routes
        if True:#update:
            self.spcost=dict(self.spcost,**newsp)
            self.routes=dict(self.routes,**newroutes)
        else:
            self.spcost=dict(self.spcost,**newsp)
            self.routes=dict(self.routes,**newroutes)

        
        
        print "\n\n1: ",self.routes
        #Eliminating neightboring paths that are broken
        for (node,link2) in self.routes.items():
            if self.getlink(link2) != None and self.getlink(link2).broken:
                print "BROKEN LINK FIXED!!!!"
                del self.routes[node]
                del self.spcost[node]
        
        print "2: ",self.routes
        print dests
        # Eliminate routes and costs for paths that go through nonexistent links    
        for (node,whatthefuckicouldhaveneamedthisanythingelse) in self.routes.items():     
            print "Node ",node," is not in dests, and the the route to ",node," from " ,self.address," is thru link ",link
            if node not in dests and self.routes[node]==link:# and node != self.address and time>40:
                print "SUCCESS"#"Node ",node," is not in dests, and the the route to ",node," from " ,self.address," is thru link ",link
                del self.routes[node]
                del self.spcost[node]
                
        print "3: ",self.routes
        #Delete links that exceed infinity
        for (node,dist) in self.spcost.items():
            if dist>=self.INFINITY:
                for (node1,dist1) in self.spcost.items():
                    if dist1>=self.INFINITY-1:
                        del self.spcost[node1]
                        del self.routes[node1]
        
        print self.address, ": final edited spcost and routes"
        print self.spcost
        print self.routes

        
        

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

 
        

