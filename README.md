# CBT - CPU BASED (ON) TTL

This CPU is based on [James Bates's design](https://www.youtube.com/watch?v=gqYFT6iecHw) however i should note that [Ben Eater's series](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU) were the initial inspiration for this project. 
Notable things about my design: 

* 16 bit memory, 1st bit decides whether we are using ROM or RAM
* Variable microtimes, SR (Step Reset) resets step counter once the instruction is done. No wasted cycles! (except NOP)
* 8/15 bit program memory, theoretically it is 15 bit though program counter is only 8 bits. programs could change HMAR themselves allowing to use more than 256 bytes.
* Program memory is stored on replaceable EEPROM which serves as cartridge in some sense,
* 32KiB of RAM,
* 256B of stack
* Stack pointer register,
* 4 general purpose registers,
* 16 ALU operations (8 logical and 8 arithmetical),
* 16*2 LCD screen as output,

## Disclaimer 

This whole project isn't actually built yet meaning that things in this repo are just ideas, therefore it might change on the way or might not be interesting for a "final user" as at its current state it contains a lot of useless information needed for microcode to be implemented.


For more specific documentation check out wiki.