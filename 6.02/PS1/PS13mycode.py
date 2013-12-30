def compress(msg, maxInput, tableSize):
    print "msg: ",msg
    """
    arguments:
    maxInput       -- a positive integer
    msg            -- a list of integers from range(maxInput)
    tableSize      -- an integer greater than maxInput
    
    outputs: a list of integers from range(tableSize)
    """
    message=[a for a in msg]
    inp =''
    code=''
    table={}
    init={}
    def init():
        t = {}
        for i in range(maxInput):
            t[str(i)]=i
        return t
    table=init()
    

    #print "Table: "
        
    while message:
        inp+=str(message.pop(0))
        print "inp: ",inp

        if inp not in table.keys():
            code = code+str(table[inp[:-1]])
            print "Added to code: ",str(table[inp[:-1]])
            print "Full Code: ", code

            print "input not in dict."
            print "Length table: ",len(table)
            print "Max len:",tableSize
            if len(table) == tableSize:
                table=init()
                table[inp]=sorted(table.values())[-1]+1
                print "Added to table: ",(inp,sorted(table.values())[-1])

            elif len(table)<tableSize:
                table[inp]=sorted(table.values())[-1]+1
                print "Added to table: ",(inp,sorted(table.values())[-1])
            else:
                table[inp]=table.values()[-1]+1
                print "CLEAR TABLE"
                print "Test 1:",table
                table = init()
                print "Test 2:", table
                table[inp]=table.values()[-1]+1               
            
            
            inp=inp[-1]
            print "Table: ",table,"\n"
            print "\nNew inp: ",inp
            print "\n###############\n"
        if len(message)==0:
            code+=str(table[inp])
    return [int(a) for a in code]



def uncompress(compressed_msg, maxInput, tableSize):
    """
    arguments:
    maxInput       -- a positive integer
    tableSize      -- an integer greater than maxInput
    nmsg        -- a list of integers from range(tableSize)

    outputs: a list of integers from range(maxInput)
    """
    def init():
        t = {}
        for i in range(maxInput):
            t[i]=str(i)
        return t
    
    table=init()
            
    msg = [a for a in compressed_msg]
    word = ''
    decoded=''
    
    for char in msg:
        print "Word: ",word
        print "Char: ",char
        if char in table.keys():
            print "CHAR"
            print "New word: ", word," + ",table[char]
            word+=table[char]
            decoded+=table[char]
        elif char == sorted(table.keys())[-1]+1:
            print "NEW VALUE"
            print "New word: ", word," + ",word+word[0]
            decoded+=word+word[0]
            word+=word+word[0]
        else:
            word=""
        

        
        print "Word: ",word
        
        b=''
        if word not in table.values():
            test=True
            while test:
                
                b+=word[0]
                #print "b....", b

                word=word[1:]
                if b not in table.values():
                    if len(table)==tableSize:
                        table=init()
                    
                    table[sorted(table.keys())[-1]+1]=b
                    print "New table:",table
                    
                    print "\nAdded: ",(sorted(table.keys())[-1],b),"\n"
                    b=b[-1]
                    
                    print "b: ", b
                else:
                    print "NO CHANGE\n"
                    print "Table: ",table
                
                        
                if len(word)==0:
                    test=False
            word=b
        

    return [int(a) for a in decoded]


    
u=[1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
c=[1, 0, 3, 0, 1, 0, 2, 1, 0, 3, 1, 3, 0, 2, 0]
c2=[1, 0, 1, 4, 1, 1, 0, 2, 1, 0, 1, 2, 0, 0, 1, 3]
#print compress(u,2,5)
print uncompress(c,2,5)
print u
