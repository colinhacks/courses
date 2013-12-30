def approximate_search(T, S):
    print "Doc: ",T
    print "Find string: ",S
    """
    Search for string S in document T. Return the position of the first match,
    or None if no match.

    Parameters
    ----------
    T : str
        Document to search.
    S : str
        String to search in document.

    Returns
    -------
    pos : int or None
        Position of first approximate match of S in T, or None if no match.
    """
    def insert(hashtable,key,element):
        try:
            hashtable[key]+=[element]
        except:
            hashtable[key]=[element]

    table={}
    substrings={}
    alphabet="abcdefghijklmnopqrstuvwxyz "
    a=263
    m=2**16-17
    k=len(S)
    n=len(T)
    d=25
    # initial hash of first substring length k
    string = T[:len(S)]
    EXP=a**(len(string)-1)
    string = T[:len(S)]
    count=0
    temp=EXP
    for t in range(k):
        count+=ord(string[t])*temp
        temp = temp/a
    insert(table, count%m,string)
    #insert(substrings, string, count%m)
    #print string  
    
    # Hashing other substrings of T with rolling hash
    temp = EXP
    val=count%m
    for offset in range(1+n-k)[1:]:
        old = string
        string=T[offset:k+offset]
        val=((val-ord(old[0])*temp)*a+ord(string[-1]))%m
        #insert(table,val,string)
        insert(substrings, string, val )
        #print string

    # Initial hash of S
    string = S
    count = 0
    temp=EXP
    for t in range(k):
        count+=ord(string[t])*temp
        temp = temp/a
    insert(table,count%m,string)
    #print string

    # Hashing all transposition variants
    S_LIST = list(S)
    INIT_VAL = count%m
    ex = EXP
    val=int(INIT_VAL)
    for i in range(k)[:-1]:
        templist=[z for z in S_LIST]
        temp = templist[i]
        templist[i]=templist[i+1]
        templist[i+1] = temp
        string = ''.join(templist)
        count = 0
        temp=EXP
        for t in range(k):
            count+=ord(string[t])*temp
            temp = temp/a
        insert(table,count%m,string)
        #print string

    # Hashing of all substitution characters
    S_LIST = list(S)
    ex = EXP
    val = int(INIT_VAL)
    for i in range(k):
        for char in alphabet:
            templist=[z for z in S_LIST]
            if not templist[i] == char:
                val = int(INIT_VAL)
                templist[i]=char
                val=(val-(ord(S[i])*ex) + (ord(char)*ex))%m
                insert(table,val,''.join(templist))
                #print ''.join(templist)
        ex = ex/a

    potentials=[]
    for key in substrings.keys():
        try:
            entry=table[substrings[key][0]]
        except:
            entry=[]
        if len(entry)>0:
            for poss in entry:
                if key==poss:
                    potentials+=[poss]
    answer=None
    for option in potentials:
        find = T.find(option)
        if answer==None or (find!=-1 and find<answer):
            answer=find
    return answer


approximate_search("washington unable to rest their eyes on a colorful photograph or boldface heading that could be easily skimmed and forgotten about americans collectively recoiled monday when confronted with a solid block of uninterrupted text dumbfounded citizens from maine to california gazed helplessly at the frightening chunk of print unsure of what to do next without an illustration chart or embedded youtube video to ease them in millions were frozen in place terrified by the sight of one long unbroken string of english words why wont it just tell me what its about said boston resident charlyne thomson who was bombarded with the overwhelming mass of black text late monday afternoon there are no bullet points no highlighted parts ive looked everywhere theres nothing here but words ow thomson added after reading the first and last lines in an attempt to get the gist of whatever the article review or possibly recipe was about at p m a deafening sigh was heard across the country as the nation grappled with the daunting cascade of syllables whose unfamiliar letteruponletter structure stretched on for an endless words children wailed for the attention of their bewildered parents businesses were shuttered and local governments ground to a halt as americans scanned the text in vain for a web link to click on sources also reported a percent rise in temple rubbing and underthebreath cursing around this time it demands so much of my time and concentration said chicago resident dale huza who was confronted by the confusing mound of words early monday afternoon this large block of text it expects me to figure everything out on my own and i hate it ive never seen anything like it said mark shelton a high school teacher from st paul mn who stared blankly at the page in front of him for several minutes before finally holding it up to his ear what does it want from us as the public grows more desperate scholars are working to randomly italicize different sections of the text hoping the italics will land on the important parts and allow everyone to go on with their day for now though millions of panicked and exhausted americans continue to repetitively search the single column of print from top to bottom and right to left looking for even the slightest semblance of meaning or perhaps a blurb some have speculated that the neverending flood of sentences may be a news article medical study urgent product recall notice letter user agreement or even a binding contract of some kind but until the news does a segment in which they take sections of the text and read them aloud in a slow calm voice while highlighting those same words on the screen no one can say for sure there are some however who remain unfazed by the virtual hailstorm of alternating consonants and vowels and are determined to ignore it im sure if its important enough theyll let us know some other way detroit local janet landsman said after all it cant be that serious if there were anything worthwhile buried deep in that block of impenetrable english it would at least have an accompanying photo of a celebrity or a large humorous title containing a pop culture reference added landsman whatever it is im pretty sure it doesnt even have a point","americant")
approximate_search("i pledge allegiance to the flag of the united states of america and to the republic for which it stands one nation und","amurica")

#approximate_search("test string","t str")
"""approximate_search("test string","storng")
"""

        
        


