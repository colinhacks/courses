
def Compute_All_Voltages(N, A):
    
    #sorting axons by start node
    axons={}
    for axon in A:
        if axon[0] in axons:
            axons[axon[0]]=axons[axon[0]]+[axon]
        else:
            axons[axon[0]]=[axon]
    
    #initializations
    voltages={}
    times={}
    for vertex in N:
        voltages[vertex[0]]='infinity'
        times[vertex[0]]=None
    voltages[0]=1
    times[0]=0

    #initialize heap
    heap = hashDictionary()
    heap.insert(0,1,"data")
    while not heap.is_empty():
        try:
            r=heap.pop()[0]
            for axon in axons[r]:
                
                if times[axon[1]] == None or times[axon[0]]+axon[2]<times[axon[1]]:
                    voltage=Blackbox(voltages[axon[0]],axon[3])
                    heap.insert(axon[1],times[axon[0]]+axon[2],"data")
                    voltages[axon[1]]=voltage
                    times[axon[1]]=times[axon[0]]+axon[2]
        except KeyError:
            pass
    return [(a,voltages[a],times[a]) for a in range(len(voltages)) if voltages[a]!='infinity']



####################
### Problem 5-3b ###
####################

######################################################################################
## N will be a list of tuples describing neurons as described previously            ##
## A will be list describing axons as described previously                          ##
## motor will be the ID of the motor neuron                                         ##
## Returned result should be a tuple (voltage, time) of the voltage and activation  ##
##   time of motor                                                                  ##
##  e.g. (23.958, 93.848)
######################################################################################

def Compute_Motor_Voltage(N, A, motor):

    axons={}
    for i in range(len(N)):
        axons[i]=[]
    for axon in A:
        axons[axon[0]]=axons[axon[0]]+[axon]
    
    #initializations
    voltages={}
    times={}
    estimates={}
    for vertex in N:
        voltages[vertex[0]]='infinity'
        times[vertex[0]]=float('inf')
        estimates[vertex[0]]=float('inf')

    k = lambda x: x[1]
    distance=calculate_distance(N[0][1],N[motor][1])
    estimates[0]=distance
    times[0]=0
    voltages[0]=1
    queue=[(0,distance)]
    while queue:
        r=queue.pop(0)
        for axon in axons[r[0]]:
            distance=times[axon[0]]+axon[2]
            if times[axon[1]] == float('inf') or distance<times[axon[1]]:
                times[axon[1]]=distance
                estimates[axon[1]]=distance+calculate_distance(N[axon[1]][1],N[motor][1])
                queue.append((axon[1],estimates[axon[1]]))
                queue=sorted(queue,key=k)
                if min(queue, key=k)[1]>times[motor]:
                    return (float(voltages[motor]),float(times[motor]))

                BB=Blackbox(voltages[axon[0]],axon[3])
                voltages[axon[1]]=BB
    return (float(voltages[motor]),float(times[motor]))
