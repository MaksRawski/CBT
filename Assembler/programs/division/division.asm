text: #d "36/4=\0"
text1: #d "165/20=\0"
addr = 0x8000

main: 
	mov sp,0xff
	mov lcdc,0x1
	mov lcdc,0xf
	mov lcdc,0x38
	
	mov cb, [text]
	mov a, 0
	call printStr

	mov b,36
	mov a,4
	call div

	; test store
	store [addr],c
	mov c,0
	load c,[addr]

	mov a,48
	add c
	mov lcd,c

	mov lcdc,0xc0
	mov cb, [text1]
	mov a, 0
	call printStr

	mov b,165
	mov a,20
	call div

	; test store
	push b
	push a

	mov ba, addr

	store [ba],c
	mov c,0
	load c,[ba]

	pop a
	pop b

	mov a,48
	add c
	mov lcd,c

	mov lcdc,0x0c

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
