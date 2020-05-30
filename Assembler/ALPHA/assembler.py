#!/bin/python3 
from opcodes import *
from formatter import *
import argparse

parser = argparse.ArgumentParser(description='Assembler for CBT in Python')

parser.add_argument('file', nargs=1, type=str, help='file to compile')
parser.add_argument('-o', '--out', nargs=1, type=str, help='output filename')

args = parser.parse_args()

if args.out:
    outName = args.out[0]
else:
    outName = 'a.out'

try:
    inFile = open(args.file[0],"r")
    fl = inFile.read()
except:
    print("Couldn't open file "+args.file[0])
    exit(1)

try:
    out = open(outName,"w")
except :
    print("Couldn't open file "+outName+" for writing")
    exit(1)

fl = frmt(fl)

buffer = [] 
labels = {} # will contain destination address
symbols = {}# will contain just the values
lines = fl.split('\n')

def errorMSG(line,msg):
	print('line '+str(line)+': '+lines[line]+' '+msg)
	exit(1)

for i in range(len(lines)):
    # lines[i] = lines[i].lower() # lowercase well not really

    # label/symbol
    if ':' in lines[i]:
        # labels[label+'.LMAR'] = 8 lower bits of address
        # labels[label+'.HMAR'] = 8 upper bits of address

        # if there is a value after a 'label' then it's a symbol
        if len(lines[i].split(":"))>=2 and lines[i].split(":")[1]!='':
            # if it's a string then convert it to array of actual values
            if len(lines[i].split("\""))>1:
                symbols[lines[i].split(':')[0]] = [ ord(elem) for elem in lines[i].split("\"")[1] ]
            else: # array of numbers
                symbols[lines[i].split(':')[0]] = [ strToNum(elem) for elem in lines[i].split(':')[1].split(',') ]
        else:
            # assign labels' values based on current length of the output buffer
            labels[lines[i][:-1]+'.LMAR'] = format(len(buffer), '04x')[2:] 
            labels[lines[i][:-1]+'.HMAR'] = format(len(buffer), '04x')[:2]

    else:
        mnemonic = lines[i].split(' ')[0]

        if mnemonic not in mnemonics.keys() and mnemonic not in ALU_OPCODES.keys():
            errorMSG(i,'Invalid mnemonic')

        if len(lines[i].split(' '))==1: # there are no arguments
            dst = False
            src = False
            translate(mnemonic, dst, src, buffer) 


        elif len(lines[i].split(' ')[1].split(','))==1: # there is one argument

            if mnemonic == ".org":
                dst = strToNum(lines[i].split(' ')[1])
                padding = dst - len(buffer)
                if padding<0:
                    errorMSG(i,".org value should be bigger than "+len(buffer)-1)
                else:
                    for i in range(padding):
                        buffer.append('00000000')
                continue # don't try to translate or do anything

            # if argument is string (label) just pass it
            if isinstance(lines[i].split(' ')[1].split(',')[0], str):
                dst = lines[i].split(' ')[1].split(',')[0]
            else:
                dst = REGISTERS[lines[i].split(' ')[1].split(',')[0]]

            src = False
            translate(mnemonic, dst, src, buffer) 

        elif len(lines[i].split(' ')[1].split(','))==2: # there are two arguments
            dst = lines[i].split(' ')[1].split(',')[0]
            src = lines[i].split(' ')[1].split(',')[1]

            # src is in symbols
            if src in symbols.keys():
                if mnemonic=="mov":
                    # put the lower part of the address aka pointer to symbol
                    srci = src+".LMAR"
                    src = 'imm'
                elif mnemonic=="load":
                    # load first value of that symbol 
                    srci = symbols[src][0]
                    # TODO: check if there is '+n' after symbol and if so access that element
                
            # if alu opcode has two arguments remove src and set it to False
            if mnemonic in ALU_OPCODES:
                src = False

            # src is an immediate opperand and wasn't altered by previous operations
            if src!=False and src not in REGISTERS.keys():
                srci = strToNum(src)
                src = 'imm'
            else:
                srci = False

            # errors
            if srci!=False and mnemonic=='push':
                errorMSG(i,'For now pushing values isn\'t supported')

            if srci!=False and mnemonic=='pop':
                errorMSG(i,'Can\'t pop into value')

            if REGISTERS[dst]==0b111:
                errorMSG(i,"Can't use immediate value as destination")
                
            if mnemonic in ALU_OPCODES and REGISTERS[dst]>3:
                errorMSG(i,'ALU can only perform operations on general purpose registers')
            
            # if there are no errors only then try to translate
            translate(mnemonic, dst, src, buffer, srci) 
        else:
            errorMSG(i,'Too many arguments')

for i in range(len(buffer)):
    try:
        x = int(buffer[i],2)
        out.write(format(x,'02x')+" ")
        print(format(x,'08b'))
        
    # evaluate labels
    except ValueError:
        if buffer[i] in labels.keys():
            out.write(labels[buffer[i]]+" ")
            print(format(int(labels[buffer[i]],16),'08b'))
        else:
            errorMSG(i,'Unrecognized label name') 

    if (i+1)%16==0:
        out.write('\n')

inFile.close()
out.close()