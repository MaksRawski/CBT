addr = 0x8000 ; addr of decimal representation of a number
delimiter = 0xff ; value stored right after the decimal number
num = 123

zero: #str "0" 

main:
	mov SP, 0xff
	mov lcdc,0x1
	mov lcdc,0xF

	mov b, num
	mov [dc],addr

	call toDec

	.printingResults
		load b,[dc]
		inc c

		; if value isn't delimiter print it
		mov a,delimiter
		cmp b
		jz .done
		
		mov a,0x30
		add b
		mov lcd,b
		jmp .printingResults


	.done
		halt

; function toDec - binary to decimal
;  b: number
;  dc: memory address to store result. 0xff delimited
toDec:
	push c

	.nextDigit:
		mov a, 10

		push c
		call div8
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


printStr:
	load d,[cb]
	inc b ; move pointer to next character
	
	cmp a,d
	jz .ret

	mov lcd,d
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
