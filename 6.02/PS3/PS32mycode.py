import sys
import numpy
import math


class Viterbi():
    def __init__(self,W):
        self.W = numpy.array(W)
        self.K = len(W[0])
        self.r = len(W)

    def back(self,x):
        stateNotation = '0'*((len(bin(self.W.shape[1]))+1)-len(bin(x)))+bin(x)[2:]
        return eval('0b'+stateNotation[1:]+'0'),eval('0b'+stateNotation[1:]+'1')

    def cost(self, bits, values):
        return sum([(x-y)**2 for x,y in zip(bits, values)])

    def bTen(self, binString):
        val = 0
        for i in xrange(len(binString)):val+=int(binString[::-1][i])*2**i
        return val

    def out_states(self,x):
        diff = self.K-1-len(bin(x))+2
        test=[a for a in bin(x)]
        test.insert(2,'0'*diff)
        binnum=''.join(test)
        return ((eval('0b0'+binnum[2:-1]),'0b0'+binnum[2:-1]),(eval('0b1'+binnum[2:-1]),'0b1'+binnum[2:-1]))

    def out(self,x):# convert x to binary, generate possible parity bits from x
        states=[a[1][2:] for a in self.out_states(x)]
        out=()
        diff = self.K-1-len(bin(x))+2
        test=[a for a in bin(x)]
        for a in range(diff):
            test.insert(2,'0')
        test=[int(d) for d in test[2:]]
        for i in [0,1]:
            num=[i]+test
            out_bits=[]
            for eq in self.W:
                out_bits.append(eq.dot(num)%2)
            out+=tuple(numpy.array([out_bits]))
        return out

    def decode(self,y):
        if (len(y)*1.0)%self.r:
            
            return (numpy.array([]),0,True)

        if self.K==1:
            unique=True
            bits=[y[self.r*i:self.r*(i+1)] for i in range(len(y)/self.r)]
            out_msg=[]
            cost_val=0.0
            for repetition in bits:
                cost_rep=self.cost(repetition,[0]*self.r)
                cost_zeroes = self.cost(repetition,[a[0] for a in self.W])
                if cost_rep >= cost_zeroes:
                    if cost_rep == cost_zeroes:
                        unique=False
                    out_msg.append(1)
                    cost_val+=self.cost(repetition,[a[0] for a in self.W])
                else:
                    out_msg.append(0)
                    cost_val +=self.cost(repetition,[0]*self.r)
            return (numpy.array(out_msg),cost_val,unique)
        
        transitions={}
        for elem in range(2**(self.K-1)):
            transitions[elem]=tuple([a[0] for a in self.out_states(elem)])
        costs=numpy.array([[(float('inf'),None,None) for i in xrange((len(y)/self.W.shape[0])+1)]]*(2**(self.W.shape[1]-1)))
        sections = 1
        while sections < 2**(self.W.shape[1]-1) and sections < 2**((len(y)/self.W.shape[0])+1):
            index = 0
            while index < 2**(self.W.shape[1]-1):
                costs[int(index)][int(math.log(sections, 2))] = (0,None,None)
                index += (2**(self.W.shape[1]-1)/sections)
            sections *= 2
        bits = int(math.log(sections, 2))
        for i in xrange(bits, (len(y)/self.W.shape[0])+1):
            for j in xrange(len(costs)):
                costs[j][i] = (0,None,None)

        changed=set()
        for i in xrange((len(y)/self.W.shape[0])):
            for t in xrange(len(costs)):
                if costs[t][i][0]==float('inf'):#(self.r+1+(self.r)*(i)):
                    pass
                else:
                    for a in [0,1]:
                        state=transitions[t][a]
                        msg_segment=[d for d in y[self.r*i:self.r*i+self.r]]
                        parity_bits=[d for d in self.out(t)[a]]
                        potential_cost=costs[t][i][0]+self.cost(msg_segment, parity_bits)
                        temp=True
                        if potential_cost<=costs[state][i+1][0]:
                            if potential_cost == costs[state][i+1][0] and costs[state][i+1][1] is not None:
                                temp=False
                            costs[state][i+1]=(potential_cost,t,temp)
                            changed.add((state,i+1))
                        elif costs[state][i+1][0]==0 and ((state,i+1) not in changed):
                            if potential_cost == costs[state][i+1][0] and costs[state][i+1][1] is not None:
                                temp=False
                            costs[state][i+1]=(potential_cost,t,temp)
                            changed.add((state,i+1))

        final_costs=[cost[-1][0] for cost in costs]
        minimum=None
        unique=True

        for a in sorted(final_costs):
            if  minimum is None:
                minimum=a
            elif a<minimum and minimum is not None:
                minimum=a
                unique=True
            elif a==minimum and minimum is not None:
                unique=False

         
        path_end=final_costs.index(minimum)
        hasChildren=True
        index=-1
        msg=[]
        while hasChildren:
            pred=costs[path_end][index][1]
            if not costs[path_end][index][2]:
                unique=False
            msg=[transitions[pred].index(path_end)]+msg
            path_end=pred
            index-=1
            if index<-(len(y)/self.W.shape[0]):
                hasChildren=False

        return (numpy.array([int(s) for s in msg]),minimum,unique)

        

if __name__ == "__main__":
    if len(sys.argv)==3:
        decoder = Viterbi(numpy.array(eval(sys.argv[1])))
        (u, Pmin, unique) = decoder.decode(numpy.array(eval(sys.argv[2])))
        print ''.join([str(x) for x in u]), \
        '   ( Pmin =',Pmin,', unique =',unique,')'
        

