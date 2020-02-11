REGISTER OPCODES
---------------
| number | register |
| --- | -- |
| %00 | ra |
| %01 | rb |
| %10 | sp |
| %11 | pc |

INSTRUCTION OPCODES
--------------------
|	instruction dst src		|	representation	|	description																				|	
|	:-----------------:		|	:-------------	|	:----------																				|
|		%0000 00 00			|	nop				|	no operation																			|
|		%0001 00 10			|	mov ra,sp		| 	move value from sp to ra																|
|		%0010 11 00			|	lod pc,[ra]		|	load to pc value at address ra															|
|		%0011 00 11			|	sto [ra],pc		|	store value in pc at address ra															|
|		%0100 00 01			|	push rb			|   put ra in [sp-1], sp stays decremented (if instruction takes one argument then use lsb) |
|		%0101 00 01			|	pop rb			|	put [sp] in rb and increment sp															|
|		%0110 00 00			|	add ra,pc		|	put the result of ra+pc in ra															|
|		%0111 00 00			|	sub ra,pc		|	put the result of ra-pc in ra															|
|		%1000 00 10			|	ldi sp,$FF		|	load immediately value $FF to sp (value is at [pc+1])									|