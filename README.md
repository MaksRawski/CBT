# CBT - CPU BASED (ON) TTL

This CPU is based on [James Bates's design](https://www.youtube.com/watch?v=gqYFT6iecHw) however 
i should note that [Ben Eater's series](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU)
was the initial inspiration for this project. Notable things about my design: 

* Variable instruction length - SR (Step Reset) resets step counter once the instruction is done,
* 15 bit program memory,
* 15 bit RAM,
* 256B of stack,
* Program memory stored on esp32 which allows programs to be uploaded remotely,
* 4 general purpose registers,
* 16 ALU operations (8 logical and 8 arithmetical),
* 2 rows 16 columns LCD output.

For documentation about specific parts check out [wiki](https://gitlab.com/MaksRawski/cbt/-/wikis/home).

## Finally done!
![CBT.jpg](CBT.jpg)
To the left of the CPU is an [esp32 which acts as ROM](https://gitlab.com/MaksRawski/esp32-as-rom). 
It replaced eariler used EEPROM.
