#include "cbt.cpu"
txt: #str "Hello, world!\0"
main:

	;init SP
	mov SP, 0xFF
	
	; init lcd
	mov lcdc, 0x1
	mov lcdc, 0xF

	mov cb, [txt] ; cb becomes pointer to txt
	mov a, 0 ; mov 0 for comparison with current character

printStr:
	load d,[cb]
	inc b ; move pointer to next character
	
	cmp a,d
	jz halt

	mov lcd,d
	jmp printStr

halt:
	hlt
