import regex
import sys

def frmt(fl):
    # format input file
    x = fl
    x = regex.sub(r';.*', r'', x) # remove comments
    x = regex.sub(r'\n\s*\n*', r'\n',x)  # remove empty lines and tabs at begginings of lines
    x = regex.sub(r'call', 'call\njmp', x) # replace call {function} with call \n jmp {function}
    x = regex.sub(r'\s*$', '', x) # remove spaces at the end of lines
    x = regex.sub(r' {2,}',' ',x)# replace all double (or more) spaces with single ones 
    x = regex.sub(r'(?<=[^\\][:,])(\ *|\\)','',x)# remove all unnecassary spaces, spaces in strings should be escaped with \  that sucks though that's how it's gonna be for a while
    x = regex.sub(r'\"\n',r'\x00"\n',x) # end strings with 0 byte
    return x

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("One file name should be given as argument")
        exit(1)
    else:
        try:
            fl = open(sys.argv[1],"r").read()
        except:
            print("Couldn't open file "+sys.argv[1])
            exit(1)
        print(frmt(fl))