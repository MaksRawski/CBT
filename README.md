# CBT - CPU BASED (ON) TTL

This CPU is based on [James Bates's design](https://www.youtube.com/watch?v=gqYFT6iecHw) however i should note that [Ben Eater's series](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU) were the initial inspiration for this project. 
Notable things about my design: 

* 16 bit memory, 1st bit decides whether we are using ROM or RAM,
* Variable instruction's length, SR (Step Reset) resets step counter once the instruction is done. No wasted cycles! (except NOP),
* 15 bit program memory,
* Program memory is stored in esp32 which allows programs to be uploaded remotely,
* 15 bit RAM,
* 256B of stack
* Stack pointer register,
* 4 general purpose registers,
* 16 ALU operations (8 logical and 8 arithmetical),
* 16*2 LCD screen as output,

For documentation about specific parts check out [wiki](https://gitlab.com/i4mz3r0/cbt/-/wikis/home).

## Finally done!
![CBT.jpg](CBT.jpg)
To the left of the actual CPU is [esp32 which acts as ROM](https://gitlab.com/MaksRawski/esp32-as-rom). 
It replaced the eariler used EEPROM.
