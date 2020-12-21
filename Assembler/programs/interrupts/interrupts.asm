
no_interrupts: #d "No interrupts received yet!\0"
recv_intrpt: #d "Received an interrupt for the\0"
end_intrpt:  #d "th time\0"

; TODO: move cursor to change the number

main:
	mov SP,0xFF
	mov lcdc,0xe

	mov dc,[no_interrupts]
	call print_MSG

	mov ba,[interrupt_handler]
	store [0xA001], b
	store [0xA002], a

	mov a,0x30
	.wait_for_interrupts:
		jmp .wait_for_interrupts
; interrupts
interrupt_handler:
	push b
	mov lcdc,0x1 ; clear screen

	load b,[0xA000] ; b has value returned by interrupt
	
	inc a

	push b

	mov b,10
	cmp a,b
	jz done ; if a is 10 then halt else continue normally
	
	pop b

	mov dc,[recv_intrpt]
	call print_MSG

	mov lcd,a

	mov dc,[end_intrpt]
	call print_MSG

	pop b
	ret

print_MSG: ; print msg with dc as a pointer to it

	push a
	push b
	mov a,0 ; initalize a with 0 for comparison with currently pointed character in string
	
	.loop:
		load b,[dc]
		cmp b,a
		
		jz .end_of_str
	inc c
	jmp .loop

	.end_of_str:
		pop b
		pop a
		ret

done:
	hlt
