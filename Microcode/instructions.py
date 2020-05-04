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

    data={
        (RO[src]|RI[dst]) #src out, dst in
    }

    if src==0 and dst==0: #nop
        data={
            0
        }

    elif src==0b110: #mov to lcd as a command
        if dst==0b111: #actual src is 111-immediate operand
            data={
                3: HPO|HAI|PCC,
                4: LPO|LAI,

                5: MO|LCE|LCM
            }
        elif dst==0b110: #00 110 110 - straight up bs
            return HLT
        else:
            data={
                3: RO[dst]|LCM|LCE # use dst as a command for lcd
            }

    elif src==0b111: #src is imm, data opcode
        data={
            3: HPO|HAI|PCC,
            4: LPO|LAI,
            5: MO|(RI[dst]) # output from memory and set control bit of input of dst
        }

    CF=(flags==0b0001)
    HF=(flags==0b0010)
    OF=(flags==0b0100)
    ZF=(flags==0b1000)

    #conditional jumps
    if dst==0b101:
        if (src==0 and CF) or (src==1 and HF) or (src==2 and OF) or (src==3 and ZF):
            data={
                #"short" register jump
                3: RO[dst]|LPI
            }
        elif src==0b111:
            #transfer of 16 bit value from memory into PC (0:instruction 1:LPC 2:HPC)
            data={
                3: LPO|LAI|PCC,
                4: HPO|HAI,
                5: MO|ALM|ALE, #dst LPC is in memory but we save it in alu

                6: LPO|LAI|PCC,
                7: HPO|HAI,
                8: MO|HPI,

                9: ALO|LPI
            }
        else:
            data={}
  
    data[len(data)+3]=SR|PCC
    return data.get(utime,0)

def load(opcode, utime, flags):

    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    data={
        3: RO[src]|LAI,
        4: RI[dst]|MO 
    }

    if src==0b111:
        #this is the same thing as 00 xxx 111 but instead of putting into PC its put into LMAR and HMAR
        data={
            3: LPO|LAI|PCC,
            4: HPO|HAI, #first byte provided is now in memory (LMAR)

            5: MO|ALM|ALE, #save LMAR into alu

            6: LPO|LAI|PCC,
            7: HPO|HAI, #second byte provided is now in memory (HMAR)

            8: MO|HAI,  #HMAR is now what it's supposed to be
            9: ALO|LAI, #LMAR is now what it's supposed to be 

            10: MO|RI[dst]
        }

    elif src==0b100:
        #pop into register
        data={ 
            3: AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
            4: ALO|HAI, #set HAI to 0xff
            5: SPO|LAI, #set LMAR to value in SP
            
            6: RI[dst]|MO,  #pop the value into dst register
            
            7: SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
            8: ALO|SPI
        }

        if dst==0b101:
            #ret
            data={
                3: AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
                4: ALO|HAI, #set HAI to 0xff
                5: SPO|LAI, #set LMAR to value in SP

                6: LPI|MO,  #pop the value into LPC

                7: SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
                8: SPI|ALO,
                9: SPO|LAI, #set LMAR to value in SP

                10: HPI|MO, #pop the other value off stack into HPC

                11: SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
                12: ALO|SPI
            }

    data[len(data)+3]=SR|PCC
    return data.get(utime,0)

def sto(opcode, utime, flags):

    dst=(opcode&0b00111000)>>3
    src=(opcode&0b00000111)>>0

    data={
            3: RO[dst]|LAI,
            4: RO[src]|MI
    }
    if dst==0b111:    
        #this is very similar thing to 01 xxx 111
        data={
            3: LPO|LAI|PCC,
            4: HPO|HAI, #first byte provided is now in memory (LMAR)

            5: MO|ALM|ALE, #save LMAR into alu

            6: LPO|LAI|PCC,
            7: HPO|HAI, #second byte provided is now in memory (HMAR)

            8: MO|HAI,  #HMAR is now what it's supposed to be
            9: ALO|LAI, #LMAR is now what it's supposed to be 

            10: MI|RO[src]
        }

    elif dst==0b100:
        #push src
        data={
            3: AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
            4: ALO|HAI, #set HAI to 0xff
            5: SPO|LAI, #set LMAR to value in SP

            6: RO[src]|MI, #push the value onto stack 

            7: SPO|AL0|AL1|AL2|AL3|ALE, #decrement SP, S=1111 M=L Cn=H
            8: SPI|ALO
        }
        if dst==0b101:
            #call
            data={
                3: AL1|AL0|ALE, #set alu to minus 1/0xFF (see 74181 docuemntation for details)
                4: ALO|HAI, #set HAI to 0xff
                5: SPO|LAI, #set LMAR to value in SP

                6: HPO|MI,  #push HPC onto stack

                7: SPO|AL0|AL1|AL2|AL3|ALE, #decrement SP, S=1111 M=L Cn=H
                8: SPI|ALO,
                9: SPO|LAI, #set LMAR to value in SP

                10: LPO|MI, #push LPC onto stack

                11: SPO|ALC|ALE, #increment SP,by default S=0000 M=L Cn=L
                12: ALO|SPI
            }

    data[len(data)+3]=SR|PCC
    return data.get(utime,0)


def alu(opcode, utime, flags):
    
    op=(opcode&0b00111100)>>2
    src=opcode&0b00000011

    CF=flags&0b0001

    ops={
        0: ALE, # NOT A
        1: AL0|ALE, # A NOR B
        2: AL2|ALE, # A NAND B
        3: AL2|AL0|ALE, # NOT B
        4: AL2|AL1|ALE, # A XOR B
        5: AL3|AL0|ALE, # A XNOR B
        6: AL3|AL1|AL0|ALE, # A AND B
        7: AL3|AL2|AL1|ALE, # A OR B

        8:  ALM|AL3|AL0|ALE, # ADD A,B
        9:  ALM|ALC*(CF^1)|AL3|AL0|ALE, # ADC A,B ALC=CF`
        10: ALM|ALC|AL2|AL1|ALE, # SUB A,B
        11: ALM|ALC*(CF)|AL2|AL1|ALE, # SBC A,B ALC=CF
        12: ALM|ALC|AL2|AL1|ALE, # CMP A,B
        13: ALM|ALC|ALE, # INC A
        14: ALM|AL3|AL2|AL1|AL0|ALE, # DEC A
        15: ALM|AL3|AL2|ALE # DBL A/SHIFT LEFT A
    }
    
    data={
        3: RO[src]|ops[op],
        4: ALO|RI[src] #output of ALU operation goes to src register
    }

    data[len(data)+3]=SR|PCC
    return data.get(utime,0)
