## REGISTER OPCODES

| opcode | register |
| --- | --|
| %000 | Ra - accumulator, result of every arithmetic operation gets stored here |
| %001 | Rb - second register of every arithmetic operation |
| %010 | Rc - general purpose register |
| %011 | Rd - general purpose register |
| %100 | SP - 8 bits wide and it's higher 8 bits are always ff |
| %101 | PC - program counter, 8 bits wide for now |
| %110 | OUT - not actual register, should only ever be used as destination for mov operations |
| %111 | imm - immediate operand |

## FLAGS

Flags are stored in 4-bit register (active high) and they are very similar (except NF) to ones used in [gameboy](https://eldred.fr/gb-asm-tutorial/flags.html). 

| Flag name        | Function                                                     |
| ---------------- | ------------------------------------------------------------ |
| CF carry flag    | set to 1 if last operation exceeded 8 bits                   |
| HF half carry    | set to 1 if carry or borrow was set out of the least significant four bits |
| NF negative flag | set to 1 if the most significant bit is 1, assumes using 2s complement |
| ZF zero flag     | set to 1 if last operation returned 0                        |

## ALU OPCODES

|                       | S3   | S2   | S1   | S0   |      | M    | Cn   |      | Function |
| --------------------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | -------- |
| LOGICAL OPERATIONS    |      |      |      |      |      |      |      |      |          |
| 0                     | 0    | 0    | 0    | 0    |      | H    | X    |      | NOT A    |
| 1                     | 0    | 0    | 0    | 1    |      | H    | X    |      | A NOR B  |
| 2                     | 0    | 1    | 0    | 0    |      | H    | X    |      | A NAND B |
| 3                     | 0    | 1    | 0    | 1    |      | H    | X    |      | NOT B    |
| 4                     | 0    | 1    | 1    | 0    |      | H    | X    |      | A XOR B  |
| 5                     | 1    | 0    | 0    | 1    |      | H    | X    |      | A XNOR B |
| 6                     | 1    | 0    | 1    | 1    |      | H    | X    |      | A AND B  |
| 7                     | 1    | 1    | 1    | 0    |      | H    | X    |      | A OR B   |
| ARITHMETIC OPERATIONS |      |      |      |      |      |      |      |      |          |
| 8                     | 1    | 0    | 0    | 1    |      | L    | H    |      | ADD A,B  |
| 9                     | 1    | 0    | 0    | 1    |      | L    | CF   |      | ADC A,B  |
| 10                    | 0    | 1    | 1    | 0    |      | L    | L    |      | SUB A,B  |
| 11                    | 0    | 1    | 1    | 0    |      | L    | CF   |      | SBC A,B  |
| 12                    | 0    | 1    | 1    | 0    |      | L    | L    |      | CMP A,B  |
| 13                    | 0    | 0    | 0    | 0    |      | L    | L    |      | INC A    |
| 14                    | 1    | 1    | 1    | 1    |      | L    | H    |      | DEC A    |
| 15                    | 1    | 1    | 0    | 0    |      | L    | H    |      | DBL A    |



## MEMORY MAP

0x0000-0x7fff ROM containing program
0x8000-0xffff(-stack size) RAM available for user
stack pointer is initialized with 0xff and its higher 8 bits are all ones

## INSTRUCTION OPCODES

This cpu has 32 instructions available though they are all based upon 4 basic operations:

%00 dst src - mov
%01 dst src - lod
%10 dst src - sto
%11 dst src - alu 

## MOVE OPERATIONS

| mnemonic      | instruction opcode    | description                                                  |
| :------------ | --------------------- | ------------------------------------------------------------ |
| nop           | %00 000 000           | moving ra to ra does absolutely nothing                      |
| mov rb,ra     | %00 001 000           | move value of register a to register b                       |
| hlt           | %00 111 111           | this opcode doesn't make sense so that's a special case of move and it will halt the computer |
| data rb, 0x2a | %00 001 111 %00101010 | data instruction is basically mov with immediate operand     |
| jmp [rb]      | %00 101 010           | jump to location at address in rb                            |
| jc [rb]       | %00 101 010           | jump carry - will jump only if carry flag is set             |
| jh [rb]       | %00 101 010           | jump half-carry - will jump only if half-carry flag is set   |
| jn [rb]       | %00 101 010           | jump negative - will jump only if negative flag is set       |
| jz [rb]       | %00 101 010           | jump zero - will jump only if zero flag is set               |

## LOAD OPERATIONS

| mnemonic    | instruction opcode | description                                               |
| ----------- | ------------------ | --------------------------------------------------------- |
| lod rc,[rb] | %01 010 001      | load value at address in rb and save it in rc |
| pop rc      |      %01 010 100      | load value at address in sp and save it in rc, increment sp (special case  of lod *,[sp], note for microcode-increment sp) |
| ret         | %01 101 100 | pop pc |



## STORE OPERATIONS

| mnemonic    | instruction opcode | description                                                  |
| ----------- | ------------------ | ------------------------------------------------------------ |
| sto [rc],rb | %10 010 001        | store value in rb at address in rc                           |
| push rc     | %10 100 010        | store value in rc at address in sp, decrement sp (special case  of sto [sp],* note for microcode-decrement sp) |
| call        | %10 100 101        | push pc - return address after function is done              |

## ALU OPERATIONS

syntax: %11 src operation opcode 
see [table above](#ALU-OPCODES) for opcodes


## EXTRA OPCODES

here are opcodes that don't make much sense which could be used for something else
-pretty much anything that uses 111 as it's dst

## TODO:

- [ ] Make this mess look any good. (ALU sections)