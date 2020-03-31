# CBT - CPU BASED (ON) TTL

Somewhat documentation for CPU based on [James Bates's design](https://www.youtube.com/watch?v=gqYFT6iecHw) however i should note that [Ben Eater's series](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU) were the initial inspiration for this project. Notable things about my design: 

* 16 bit memory, 1st bit decides whether we are using ram or rom
* 8/15 bit program memory, theoretically it is 15 bit though program counter is only 8 bits. "cheating" is required to use more than 256 bytes. Program memory is stored on replaceable EEPROM which serves as cartridge in some sense,
* 15 bit user memory, first bit is used to indicate whether access is given to ram or rom, 
* 4 general purpose registers,
* 16 ALU operations (8 logical and 8 arithmetical),
* Stack pointer register,
* 16*2 LCD screen as output,

## Disclaimer 

This whole project isn't actually built yet meaning that things in this repo are just ideas, therefore things in here might change on the way or might not be interesting for a "final user" as at its current state it contains information needed for microcode to be implemented.


For more specific documentation check out wiki.