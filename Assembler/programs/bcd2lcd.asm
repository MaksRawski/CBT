; code stolen from https://cpu.visualrealmsoftware.com/asm/#
; binary to decimal lcd example
; modified to suit cbt instruction set

; Convert an 8-bit binary number into decimal digits
; and output digits to the display

;NUMBER = 135
;ADDR   = 0
;TERMINATOR = 255
zero: #str "0" 

main:
	mov SP, 0xff
	mov lcdc,0x1
	mov lcdc,0xe

	mov d, 135
	mov b,d
	; instruction below could be removed
	mov a, 0 

	call toDec8
	
	.output:
		call printResult
		jmp .output

printResult:
    mov lcdc,0x1
	mov a,0
	mov b,0xff
	mov d, 135
	
	.findEnd:
		load Rc, Ra
		cmp Rb, Rc
		jz .startPrint
		inc Ra
		jmp .findEnd

	.startPrint:
		data Rc, ADDR
	
	.nextDigit:
		dec Ra
		lod Rd, Ra
		data Rb, ZERO
		add Rd
		lcd Rd
		mov Rb, Ra
		cmp Rb, Rc
		jz .return
		jmp .nextDigit
	
	.return:
		ret


; function toDec - binary to decimal
;  Rb: number
;  Ra: memory address to store result. 0xff delimited
toDec8:
	push Ra
	push Rb
	
	.nextDigit:
		pop Ra  ; get remaining number
		data Rb, 10
		call div8
		pop Rb  ; address to Rb
		sto Rb, Ra ; store remainder
		inc Rb
		push Rb  ; push next memory address
		tst Rc
		jz .return
		push Rc
		jmp .nextDigit

	.return:
		pop Rb
		data Ra, TERMINATOR  ; add terminator
		sto Rb, Ra
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

div8:
	mov c, 0x00
	
	.add:
		inc c

		; b=b-a
		sub b,a
		jz .return
		jc .return

		jmp .add

	.return:
		ret
