#include "cbt.cpu"
mov rb,0x2a
.print:
	mov lcdc,0xe
	mov lcd,rb
jmp .print
hlt
