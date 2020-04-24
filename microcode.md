## notes for microcode 
* control word is 31 bits wide.
* active low except MI, PCC and ALU inputs

## Control word

HLT - HALT<br/>
LAI - LOW ADDRESS IN<br/>
HAI - HIGH ADDRESS IN<br/>
MO - MEMORY OUT<br/>
'MI - 'MEMORY IN<br/>
II - INSTRUCTION (REGISTER) IN<br/>
IO - INSTRUCTION (REGISTER) OUT<br/>
SR - STEP RESET<br/>
PCO - PROGRAM COUNTER OUT<br/>
'PCC - 'PROGRAM COUNTER COUNT<br/>
PCI - PROGRAM COUNTER IN<br/>
SPO - STACK POINTER OUT<br/>
SPI - STACK POINTER IN<br/>
AO - A (REGISTER) OUT<br/>
AI - A (REGISTER) IN<br/>
CO - C (REGISTER) OUT<br/>
CI - C (REGISTER) IN<br/>
ALO - ALU (buffer) OUT <br/>
ALE - ALU ENABLE-save ALU output to buffer<br/>
AL3 - ALU S3<br/>
AL2 - ALU S2<br/>
AL1 - ALU S1<br/>
AL0 - ALU S0<br/>
ALM - ALU MODE<br/>
ALC - ALU CARRY IN<br/>
BO - B (REGISTER) OUT<br/>
BI - B (REGISTER) IN<br/>
DO - D (REGISTER) OUT<br/>
DI - D (REGISTER) IN<br/>
LCM - LCD MODE,<br/>
LCE - LCD ENABLE<br/>
<br/>
**for 8 bit PC:**<br/>
HLT, LAI, HAI, MO, 'MI, II, IO, SR, PCO, 'PCC, PCI, SPO, SPI, AO, AI, CO, CI, ALO, ALE, AL3, AL2, AL1, AL0, ALM, ALC, BO, BI, DO, DI, LCM, LCE
<br/>31 control bits<br/>

<br/>
**for 16 bit PC:**<br/>
HLT, LAI, HAI, MO, 'MI, II, IO, LPCO, 'PCC, LPCI, HPC0, HPCI, AO, AI, CO, CI, ALO, ALE, AL3, AL2, AL1, AL0, ALM, ALC, BO, BI, DO, DI, LCM, LCE, SPO, SPI
<br/>32 control bits