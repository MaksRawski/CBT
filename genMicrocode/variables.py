#control word
HLT=1<<0
LAI=1<<1
HAI=1<<2
MO=1<<3
MI=1<<4
II=1<<5
IO=1<<6
SR=1<<7
PCO=1<<8
PCC=1<<9
PCI=1<<10
SPO=1<<11
SPI=1<<12
AO=1<<13
AI=1<<14
CO=1<<15
CI=1<<16
ALO=1<<17
ALE=1<<18
AL3=1<<19
AL2=1<<20
AL1=1<<21
AL0=1<<22
ALM=1<<23
ALC=1<<24
BO=1<<25
BI=1<<26
DO=1<<27
DI=1<<28
LCM=1<<29
LCE=1<<30

RI=(
    AI,   #000
    BI,   #001
    CI,   #010
    DI,   #011
    SPI,  #100
    PCI,  #101
    LCE,  #110
    LAI   #111
)

RO=(
    AO,   #000
    BO,   #001
    CO,   #010
    DO,   #011
    SPO,  #100
    PCO,  #101
    000,  #110
    000   #111
)
DATA=[0]*65536