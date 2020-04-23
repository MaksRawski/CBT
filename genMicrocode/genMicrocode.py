from instructions import *

# address is composed as so
# FLAGS  MICROTIME INSTRUCTION REGISTER
#  xxxx     xxxx     xxxx xxxx

#addData actually writes data
#opcode,ut and flag are just for getting address
for opcode in range(2**8):
    for ut in range(2**4):
        for flag in range(2**4):
            if ut in [0,1]: #first 2 steps of every instruction is to actually fetch it
                addData(fetch(ut),opcode,ut,flag)
            else: #instructions above never are run with ut=0 or ut=1
                addData({
                0: mov,
                1: load,
                2: sto,
                3: alu,
                }[opcode>>6](opcode,ut,flag),
                opcode,ut,flag)
    if (opcode+1)%64==0:
        print("Writing "+{
        0: "mov's",
        1: "load's",
        2: "store's",
        3: "alu's"
    }[opcode>>6])

# DATAFILE=open("microcode/microcode","w")
p=(
    open("microcode/microcode.p0","w"),
    open("microcode/microcode.p1","w"),
    open("microcode/microcode.p2","w"),
    open("microcode/microcode.p3","w") #highest 8 bits, most to left EEPROM
)

for i in range(len(DATA)-1):
    for j in range(4):
        p[j].write(
        hex((DATA[i]>>(8*j))&0xff)[2:]
        )
        p[j].write(" ")
        if (i+1)%16==0:
            p[j].write("\n")

for i in range(4):
    p[i].close()