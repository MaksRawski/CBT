; function div8 - divide two 8-bit integers
;  b: dividend
;  a: divisor
; returns:
;  c: result
;  b: remainder

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

	hlt

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
	
	.step:
		cmp b,a
		;jz .return
		jc .add ; if there is carry it means there is no borrow therefore we continue subtracting
		jmp .return
		
	.add:
		inc c
		; b = b - a
		sub b
		jz .return
		jmp .step

	.return:
		ret
