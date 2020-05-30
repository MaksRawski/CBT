main:
	mov sp,0xFF ; init SP
	call lcd_init ; push onto stack current LMAR and later HMAR and then set LMAR and HMAR to the address where lcd_init is

	mov ra,2
	mov rb,2
	add rb,ra ; ra has to be an input for ALU operations (might be unspecificed though)
	; result is in rb
	mov ra,0b00110000
	add rb,ra ; value for lcd in rb

	mov lcd,rb
	hlt

lcd_init:
	mov lcdc,0x1
	mov lcdc,0xe
	ret