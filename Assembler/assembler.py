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
labels = {}
symbols = {}
lines = fl.split('\n')

def errorMSG(line,msg):
	print('line '+str(line)+': '+lines[line]+' '+msg)
	exit(1)



for i in range(len(lines)):
    lines[i] = lines[i].lower() # lowercase 

    if ':' in lines[i]:
        # labels[label+'.LMAR'] = 8 lower bits of address
        # labels[label+'.HMAR'] = 8 upper bits of address
        # if there is a value after a 'label' then it's a symbol
        if len(lines[i].split(":"))>=2 and lines[i].split(":")[1]!='':
            symbols[lines[i].split(':')[0]] = lines[i].split(':')[1]
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

            # if argument is label just pass it
            if isinstance(lines[i].split(' ')[1].split(',')[0], str):
                dst = lines[i].split(' ')[1].split(',')[0]
            else:
                dst = REGISTERS[lines[i].split(' ')[1].split(',')[0]]

            src = False
            translate(mnemonic, dst, src, buffer) 

        elif len(lines[i].split(' ')[1].split(','))==2: # there are two arguments
            dst = lines[i].split(' ')[1].split(',')[0]
            src = lines[i].split(' ')[1].split(',')[1]

            # if alu opcode has two arguments remove src and set it to False
            if mnemonic in ALU_OPCODES:
                src = False

            # src is an immediate opperand
            if src!=False and src not in REGISTERS.keys():
                if src.isdigit():
                    srci = int(src,10) 
                    src = 'imm'

                elif src[1:]=='$' or src[:2]=='0x' or src[-1:]=='h':
                    srci = int(src,16)
                    src = 'imm'

                elif src[1:]=='%' or src[:2]=='0b' or src[-1:]=='b':
                    srci = int(src,2)
                    src = 'imm'

            # errors
            if srci!=False and mnemonic=='push':
                errorMSG(i,'For now pushing values isn\'t supported')

            if srci!=False and mnemonic=='pop':
                errorMSG(i,'Can\'t pop into value')

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