from variables import *

#TODO: make sure that all unused opcodes eg. 01 000 110 end up being just SR|PCC
# problem with this microcode is that jumping can't be done to addresse farer away than 256 bytes. Jump on {flag} can only change LMAR
# fixed though now a lot of things take waaaaaay more cycles

#invert all inputs despite MI, PCC, ALU inputs and obviously the one(s) given that should be activated
def CW(x):
    return int(x)^((2**31-1)^MI^PCC^AL0^AL1^AL2^AL3)

def addData(data,opcode,ut,flag):
    DATA[(flag<<12)+(ut<<8)+(opcode)]=CW(data)


#these opcode functions just return data
def fetch(utime):
    return{
        0: LPO|LAI,
        1: HPO|HAI,
        2: II|MO
    }[utime]


def mov(opcode, utime, flags):

    #for easy selection of parts of opcodes
    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    data=[
        (RO[src]|RI[dst]) #src out, dst in
    ]

    if src==0 and dst==0: #nop
        data=[
            0
        ]

    elif src==0b110: #mov to lcd as a command
        if dst==0b111: #actual src is 111-immediate operand
            data=[
                HPO|HAI|PCC,
                LPO|LAI,

                MO|LCE|LCM
            ]
        elif dst==0b110: #00 110 110 - straight up bs
            return HLT
        else:
            data=[
                RO[dst]|LCM|LCE # use dst as a command for lcd
            ]

    elif src==0b111: #src is imm, data opcode
        data=[
            HPO|HAI|PCC,
            LPO|LAI,
            MO|(RI[dst]) # output from memory and set control bit of input of dst
        ]

    CF=(flags==0b0001)
    HF=(flags==0b0010)
    OF=(flags==0b0100)
    ZF=(flags==0b1000)

    #conditional jumps
    if dst==0b101:
        if (src==0 and CF) or (src==1 and HF) or (src==2 and OF) or (src==3 and ZF) or (src==0b111):
            data=[
                LPO|LAI|PCC,
                HPO|HAI,
                MO|ALM|ALE, #dst LPC is in memory but we save it in alu

                LPO|LAI|PCC,
                HPO|HAI,
                MO|HPI,

                ALO|LPI
            ]
        else:
            data=[]
  
    data.append(SR|PCC)
    try:
        return data[utime]
    except IndexError:
        return SR|PCC

def load(opcode, utime, flags):

    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    data=[
        RO[src]|LAI,
        RI[dst]|MO 
    ]

    if src==0b111:
        #this is the same thing as 00 xxx 111 but instead of putting into PC its put into LMAR and HMAR
        data=[
            LPO|LAI|PCC,
            HPO|HAI, #first byte provided is now in memory (LMAR)

            MO|ALM|ALE, #save LMAR into alu

            LPO|LAI|PCC,
            HPO|HAI, #second byte provided is now in memory (HMAR)

            MO|HAI,  #HMAR is now what it's supposed to be
            ALO|LAI, #LMAR is now what it's supposed to be 

            MO|RI[dst]
        ]

    elif src==0b100:
        #pop into register
        data=[ 
            AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
            ALO|HAI, #set HAI to 0xff
            SPO|LAI, #set LMAR to value in SP
            
            RI[dst]|MO,  #pop the value into dst register
            
            SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
            ALO|SPI
        ]

        if dst==0b101:
            #ret
            data=[
                AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
                ALO|HAI, #set HAI to 0xff
                SPO|LAI, #set LMAR to value in SP

                LPI|MO,  #pop the value into LPC

                SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
                SPI|ALO,
                SPO|LAI, #set LMAR to value in SP

                HPI|MO, #pop the other value off stack into HPC

                SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
                ALO|SPI
            ]

    data.append(SR|PCC)
    try:
        return data[utime]
    except IndexError:
        return SR|PCC

def sto(opcode, utime, flags):

    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    data=[
            RO[dst]|LAI,
            RO[src]|MI
    ]
    if dst==0b111:    
        #this is very similar thing to 01 xxx 111
        data=[
            LPO|LAI|PCC,
            HPO|HAI, #first byte provided is now in memory (LMAR)

            MO|ALM|ALE, #save LMAR into alu

            LPO|LAI|PCC,
            HPO|HAI, #second byte provided is now in memory (HMAR)

            MO|HAI,  #HMAR is now what it's supposed to be
            ALO|LAI, #LMAR is now what it's supposed to be 

            MI|RO[src] #store src
        ]

    elif dst==0b100:
        #push src
        data=[
            AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
            ALO|HAI, #set HAI to 0xff
            SPO|LAI, #set LMAR to value in SP

            RO[src]|MI, #push the value onto stack 

            SPO|AL0|AL1|AL2|AL3|ALE, #decrement SP, S=1111 M=L Cn=H
            SPI|ALO
        ]
        if dst==0b101:
            #call
            data=[
                AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
                ALO|HAI, #set HAI to 0xff
                SPO|LAI, #set LMAR to value in SP

                HPO|MI,  #push HPC onto stack

                SPO|AL0|AL1|AL2|AL3|ALE, #decrement SP, S=1111 M=L Cn=H
                SPI|ALO,
                SPO|LAI, #set LMAR to value in SP

                LPO|MI, #push LPC onto stack

                SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
                ALO|SPI
            ]

    data.append(SR|PCC)
    try:
        return data[utime]
    except IndexError:
        return SR|PCC


def alu(opcode, utime, flags):
    
    op=(opcode&0b00111100)>>2
    src=opcode&0b00000011

    CF=flags&0b0001

    ops=[
        ALE, # NOT A
        AL0|ALE, # A NOR B
        AL2|ALE, # A NAND B
        AL2|AL0|ALE, # NOT B
        AL2|AL1|ALE, # A XOR B
        AL3|AL0|ALE, # A XNOR B
        AL3|AL1|AL0|ALE, # A AND B
        AL3|AL2|AL1|ALE, # A OR B

        ALM|AL3|AL0|ALE, # ADD A,B
        ALM|ALC*(CF^1)|AL3|AL0|ALE, # ADC A,B ALC=CF`
        ALM|ALC|AL2|AL1|ALE, # SUB A,B
        ALM|ALC*(CF)|AL2|AL1|ALE, # SBC A,B ALC=CF
        ALM|ALC|AL2|AL1|ALE, # CMP A,B
        ALM|ALC|ALE, # INC A
        ALM|AL3|AL2|AL1|AL0|ALE, # DEC A
        ALM|AL3|AL2|ALE # DBL A/SHIFT LEFT A
    ]
    
    data=[
        RO[src]|ops[op],
        ALO|RI[src] #output of ALU operation goes to src register
    ]

    data.append(SR|PCC)
    try:
        return data[utime]
    except IndexError:
        return SR|PCC
