import sys
import PS13mycode

if __name__ == "__main__":
    nargin = len(sys.argv)
    if nargin == 1:
        print """
usage:
python PS1lzw.py filename
python PS1lzw.py u filename
              """
    else:
        filename = sys.argv[1]
        input_file = open(filename,'rb')
        msg = [ord(x) for x in input_file.read()]
        input_file.close()
        if nargin == 2:
            cmsg = PS13mycode.compress(msg,256,65536)
            newmsg = ''.join(["%s%s"%(chr(x/256),chr(x%256)) for x in cmsg])
            newfile = filename+'.zl'
        else:
            cmsg = [256*msg[i]+msg[i+1] for i in xrange(0,len(msg),2)]
            umsg = PS13mycode.uncompress(cmsg,256,65536)
            newmsg = ''.join([chr(x) for x in umsg])
            newfile = filename+'.u'
        output_file = open(newfile,'wb')
        output_file.write(newmsg)
        output_file.close()
