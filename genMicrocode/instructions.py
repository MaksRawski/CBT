from variables import *

#invert all inputs despite MI, PCC, ALU inputs and obviously the one(s) given that should be activated
def CW(x):
    return int(x)^((2**31-1)^MI^PCC^AL0^AL1^AL2^AL3^ALM)

def addData(data,opcode,ut,flag):
    DATA[(flag<<12)+(ut<<8)+(opcode)]=CW(data)


#these opcode functions just return data
def fetch(utime):
    return{
        0: PCO|LAI,
        1: II|MO|PCC
    }[utime]


def mov(opcode, utime, flags):
    #end every instruction with SR (step reset) otherwise they would take 16 steps and there might be other unexpected behaviour

    #for easy selection of parts of opcodes
    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    if opcode==0b00000000: #nop
        data={
            2: 0
        }

    elif src==0b110: #src is lcd but reading from lcd is impossible therefore halt (for every ut)
        return HLT

    elif src==0b111: #src is imm, data opcode
        data={
            2: PCC,
            3: PCO|LAI,
            4: MO|(RI[dst]) # output from memory and set control bit of input of dst
        }
   
    else:
        data={
            2: (RO[src]|RI[dst]) #src out, dst in
        }

    data[len(data)+2]=SR
    return data.get(utime,0)

def load(opcode, utime, flags):

    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    CF=(flags&0b0001)>>0
    HF=(flags&0b0010)>>1

    if src==0b110:
        if CF:
            data={2: RO[dst]|PCI}
        else:
            data={}

    elif src==0b111:
        if HF:
            data={2: RO[dst]|PCI}
        else:
            data={}


    elif src==0b100:
        data={
            2: AL1|AL0|ALE, #set alu to minus 1
            3: ALO|HAI, #set HAI to 0xff
            4: RO[src]|LAI,
            5: RI[dst]|MO,
            6: SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
            7: ALO|SPI
        }

    else:
        data={
            2: RO[src]|LAI,
            3: RO[dst]|MO
        }

    data[len(data)+2]=SR
    return data.get(utime,0)

def sto(opcode, utime, flags):

    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    OF=(flags&0b0100)>>2
    ZF=(flags&0b1000)>>3

    if src==0b110:
        if OF:
            data={2: RO[dst]|PCI}
        else:
            data={}

    if src==0b111:
        if ZF:
            data={2: RO[dst]|PCI}
        else:
            data={}

    elif dst==0b100:
        data={
            2: AL1|AL0|ALE, #set alu to minus 1 (0xff)
            3: ALO|HAI, #set HAI to 0xff
            4: RO[dst]|LAI,
            5: RI[src]|MI,
            6: SPO|AL0|AL1|AL2|AL3|ALE, #decrement SP, S=1111 M=L Cn=H
            7: ALO|SPI
        }

    else:
        data={
            2: RO[dst]|LAI,
            3: RO[src]|MI
        }

    data[len(data)+2]=SR
    return data.get(utime,0)


def alu(opcode, utime, flags):
    
    op=(opcode&0b00111100)>>2
    src=opcode&0b00000011

    CF=flags&0b0001

    ops={
        0: ALM|ALE, # NOT A
        1: ALM|AL0|ALE, # A NOR B
        2: ALM|AL2|ALE, # A NAND B
        3: ALM|AL2|AL0|ALE, # NOT B
        4: ALM|AL2|AL1|ALE, # A XOR B
        5: ALM|AL3|AL0|ALE, # A XNOR B
        6: ALM|AL3|AL1|AL0|ALE, # A AND B
        7: ALM|AL3|AL2|AL1|ALE, # A OR B

        8:  AL3|AL0|ALE, # ADD A,B
        9:  (ALC*(CF^1))|AL3|AL0|ALE, # ADC A,B ALC=CF`
        10: ALC|AL2|AL1|ALE, # SUB A,B
        11: (ALC*(CF))|AL2|AL1|ALE, # SBC A,B ALC=CF
        12: ALC|AL2|AL1|ALE, # CMP A,B
        13: ALC|ALE, # INC A
        14: AL3|AL2|AL1|AL0|ALE, # DEC A
        15: AL3|AL2|ALE # DBL A/SHIFT LEFT A
    }
    
    data={
        2: RO[src]|ops[op],
        3: ALO|RI[src] #output of ALU operation goes to src register
    }

    data[len(data)+2]=SR
    return data.get(utime,0)
