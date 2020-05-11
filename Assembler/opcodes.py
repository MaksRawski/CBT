mnemonics = {
	'nop': '00000000',
	'mov': '00dstsrc',
	'hlt': '00110110',
	'jmp': '00101111',
	'jc':  '00101000',
	'jh':  '00101001',
	'jo':  '00101010',
	'jz':  '00101011',

	'load':'01dstsrc',
	'pop': '01dst100',
	'ret': '01101100',

	'store':'10dstsrc',
	'push': '10100src',
	'call': '10100101'
}

REGISTERS = {
	'ra':0b000,
	'a': 0b000,

	'rb':0b001,
	'b': 0b001,
	
	'rc':0b010,
	'c': 0b010,

	'rd':0b011,
	'd': 0b011,

	'sp':0b100,

	'pc':0b101,
	
	'lcd': 0b110,

	'imm': 0b111
}

ALU_OPCODES = {
		"not": 0b0000,
		"nor": 0b0001,
		"nand":0b0010,
		"xor": 0b0100,
		"xnor":0b0101,
		"and": 0b0110,
		"or":  0b0111,

		"add": 0b1000,
		"adc": 0b1001,
		"sub": 0b1010,
		"sbc": 0b1011,
		"cmp": 0b1100,
		"inc": 0b1101,
		"dec": 0b1110,
		"dbl": 0b1111
}

def translate(mnemonic, dst, src, buffer, srci=False):

	if dst==False and src==False: # nop hlt ret call
		buffer.append(mnemonics[mnemonic])

	else:
		# put actual src or data in place of template
		# unless it's label/string
		mnem = False
		if mnemonic in mnemonics:
			mnem = mnemonics[mnemonic]

			if dst == 'lcdc': # move to lcd as command, replace src with dst and vice versa
				dst = src
				src = 'lcd'

			if dst in REGISTERS:
				mnem = mnem.replace('dst',str(bin(REGISTERS[dst])[2:].zfill(3))) 

			if src in REGISTERS:
				mnem = mnem.replace('src',str(bin(REGISTERS[src])[2:].zfill(3))) 

			
		elif mnemonic in ALU_OPCODES:
			mnem = ALU_OPCODES[mnemonic]
			if dst in REGISTERS:
				mnem = bin((0b11<<6)+(ALU_OPCODES[mnemonic]<<2)+(REGISTERS[dst])).zfill(8)[2:]

		if mnem!=False:
			buffer.append(mnem)

		if mnemonic in [ # jumps
			"jmp",
			"jc",
			"jh",
			"jo",
			"jz",
		]:
			buffer.append(dst+".LMAR")
			buffer.append(dst+".HMAR")

		elif mnemonic in [ # push pop operations
			'pop', # can't pop into value
			'push' # and for now also can't push values
		]:
			if srci!=False:
				buffer.append(srci)

		elif mnemonic in [
			'mov',
		]:
		# check if src is imm
			if srci!=False: # there is value for an immediate opcode, src=0b111
				buffer.append(format(srci,'08b'))
		elif (mnemonic == 'load' and REGISTERS[src] == 0b111) or (mnemonic == 'store' and REGISTERS[dst] == 0b111):
			# do similar magic to jumps but with 'variables'
			pass