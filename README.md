# CBT - CPU BASED (ON) TTL

Somewhat documentation for CPU based on [James Bates's design](https://www.youtube.com/watch?v=gqYFT6iecHw) however i should note that [Ben Eater's series](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU) was the initial inspiration for this project. Notable things about my design: 

* 8 bit program memory, theoretically it is 16 bit though program counter is only 8 bits. Program memory is stored on replaceable EEPROM which serves as cartridge in some sense,
* 15 bit user memory, first bit is used to indicate whether access is given to ram or rom, 
* 4 general purpose registers, though ALU operations can only be performed on ra and rb,
* 16 ALU operations (8 logical and 8 arithmetical),
* Stack pointer register,
* 16*2 LCD screen as output,

For more specific documentation check out wiki.