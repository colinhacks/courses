def encode(codeBook, msg):
    """
    arguments:
    codeBook -- list of 0/1 strings (e.g. the output of PS11mycode.huffman)
    msg      -- list of integers between 0 and len(codeBook)
    
    returns: 0/1 string
    """
    print codeBook
    code =''
    for char in msg:
        code+=codeBook[int(char)]
        print "Char: " ,char
    return code
    
def decode(codeBook, msg):
    """
    arguments:
    codeBook -- list of 0/1 strings, prefix-free (e.g. from PS11mycode.huffman)
    msg      -- encoded message (a 0/1 string)
    
    returns: list of integers between 0 and len(codeBook)
    """
    word=""
    real=[]
    while msg:
        word+=msg[0]
        msg=msg[1:]
        if word in codeBook:
            real.append(codeBook.index(word))
            word=''
        else:
            pass
    return real
            
