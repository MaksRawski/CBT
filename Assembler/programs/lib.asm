delimiter = 0xff

; takes:
; 	[cb]: as a pointer to string
; returns:
; 	to lcd
printStr:
	load d,[cb]
	inc b ; move pointer to next character
	
	cmp a,d
	jz .ret

	mov lcd,d
	jmp printStr

	.ret:
		ret

; takes:
; 	b: dividend
; 	a: divisor
; returns
; 	c: quotient
; 	d: remainder
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

; takes:
; 	b: number
; 	[dc]: memory address to store result.
; returns:
; 	at [dc] the result is delimited with variable delimiter
toDec:
	push c

	.nextDigit:
		mov a, 10

		push c
		call div
		mov a,c ; mov result of division into a
		pop c

		store [dc],a
		inc c

		push b
		mov b,0
		cmp b ; if the result of division is 0 
			  ; it means that the number is smaller than 10

		jz .return

		pop b
		jmp .nextDigit

	.return:
		pop b

		store [dc],delimiter
		pop c
		; dc is what it was before the function was run

		ret

