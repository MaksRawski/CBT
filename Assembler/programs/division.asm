; function div8 - divide two 8-bit integers
;  Rb: dividend
;  Ra: divisor
; returns:
;  Rc: result
;  Rb: remainder

#include "cbt.cpu"
text: #str "8/2=\0"
main: 
	mov sp,0xff
	mov lcdc,0x1
	mov lcdc,0xf
	
	mov cb, [text]
	mov a, 0
	call printStr

	mov b,8
	mov a,2
	call div8

	mov a,48
	add c
	mov lcd,c

printStr:
	load d,[cb]
	inc b ; move pointer to next character
	
	cmp a,d
	jz .ret

	mov lcd,d
	jmp printStr

	.ret:
		ret

div8:
	mov c, 0x00
	
	.add:
		inc c

		; b=b-a
		sub b,a
		jz .ret
		jc .add ; if there is carry it means there is no borrow therefore we continue subtracting
		jmp .ret ; if there was borrow then b is smaller than 0

	.ret:
		ret
