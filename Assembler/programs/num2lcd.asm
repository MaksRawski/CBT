#include "cbt.cpu"

addr = 0x8000 ; addr of decimal representation of a number
delimiter = 0xff ; value stored right after the decimal number
num = 123

main:
	mov SP, 0xff
	mov lcdc,0x1
	mov lcdc,0xF
	mov lcdc,0x38

	mov b, num
	mov dc,addr
	call toDec

	call printStr
	mov lcdc, 0x0c
	halt
	
		

; function toDec - binary to decimal
;  b: number
;  dc: memory address to store result. in that address will be delimiter
; reading should be backwards, subtracting till you reach the delimiter
; [dc+1] has the last digit
; this function will set dc to point at first digit

; TODO check if  div returns correct remainder
toDec:
	; setup result address
	push a
	mov a,delimiter

	store [dc],a
	inc c

	mov a,10
	.while:
		push c
		push d

		call div
		; quotient goes to c
		; remainder goes to b

		; mov remainder to a
		; mov quotient to b
		mov a,b
		mov b,c

		; get address back to dc
		pop d
		pop c
		
		; store remainder at dc
		store [dc], a
		inc c
		
		; check if quotient is less than ten
		; if it is then store it in dc and ret
		mov a,10
		cmp b,a

		; if there is carry it means there is no borrow
		; therefore quotient is bigger than 10 
		; and we continue the loop
		jc .while

	; else
	store [dc], b
	pop a
	ret

printStr:
	; dc has the first digit and we decrement c
	; until we have delimiter

	load b,[dc]
	dec c
	
	; cmp current character with delimiter
	mov a,delimiter
	cmp a,b
	jz .ret

	; add 0x30 to convert it to ascii
	; and print it
	mov a,0x30
	add b
	mov lcd,b
	jmp printStr

	.ret:
		ret

div:
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
