
************************************************************************************
                                         BioNES

                                                        NES emulator for Wiondows 95
                                                                            Freeware
                                                                         Version 0.2
                                                              Main Author: Shu Kondo
                                                    Technical Assistant: FanWen Yang
************************************************************************************


--------------
 Introduction
--------------

    BioNES is a NES emulator for Windows 95. It requires DirectX 3.0 or higher.
    It is highly optimized for MMX technology, but it works fine on non-MMX
    Pentium processors, too.


----------
 Features
----------

    o Almost everything is manually optimized for MMX technology
    o 100% ASM 6502 core
    o All 5 sound channels
    o Namcot custom sound channels (Megami Tensei 2, Final Lap, etc...)
    o Namcot custom Save RAM (saved in .nmc files)
    o Good MMC5 support
    o MMC5 custom sound channels
    o Konami VRC6 custom sound channels
    o Konami VRC7 custom sound channels (partial)
    o 16-bit color graphics engine
    o Correct palette manipulation (Wizards and Warriors)
    o Correct sprite priority (MMX users only)
    o Support for NES hardware interrupt
    o Support for the following mappers
      iNES mappers: 0,1,2,3,4,5,7,8,9,10,11,15,16,17,18,19,21,22,23,24,25,26,32,33,34
      fwNES mappers: 65,66,67,68,69,70,72,73,75,76,77,78,80,82,85,86,87,88,89,92
      BioNES mappers: 93,94,95,97
    o Joypad


--------
  Keys
--------

    Up, Down, Right, Left: Arrow Keys
    Start: [Enter]
    Select: [Tab]
    A: [Left-Alt], [Z], [.]
    B: [Ctrl], [Left-Shift], [0]
    * 2P Microphone: [M]
    ** HyperShot Dash: [D]
    ** HyperShot Jump: [F]
    SoftReset: [R]
    Switch screen mode: [F1]
    Decrease frameskip: [F2]
    Increase frameskip: [F3]
    Enable/Disable joypad reading: [F4]
    Realtime Save: [F5] (Hold down [0]...[9] to select slot)
    Show/Hide FPS: [F6]
    Realtime Load: [F7]

    * The Japanese NES comes with a microphone on the second controller.
    * HyperShot is a custom controlling device from Konami.
      I don't know if it was ever released outside of Japan.


------
 ROMz
------

    In order to play games, you must obtain ROM images separately.
    The author NEVER distributes ROM images, since it's a vilation of the
    copyright law. Nor does the author tell you where you can find illegally
    reproduced ROM images.
    You are supposed to dump ROM images using extracting devices like IO-56.
    If you are having any specific problem dumping ROM images (especially
    Japanese ROMs), feel free to contact me.

    I will NOT send you ROMs.
    I will NOT distribute ROMs with BioNES.
    I will NOT dump ROMs for you.
    I will NOT tell you where to find ROMs.


-----------------
 NES File Header
-----------------

    Once you dump a ROM image, you must attache a proper header.
    Its format is as follows:

    Byte Number
　　0: $4E (File Identification)
    1: $45 (File Identification)
    2: $53 (File Identification)
    3: $1A (File Identification)
    4: Porgram data size (bytes) / 16384
    5: Character data size (bytes) / 8192
    6:
        Bit 0: Mirroring (0 = Horizontal, 1 = Vertical)
　　　　Bit 1: Presence of battery-backed SRAM
        Bit 2: Presence of Trainer (Patch)
        Bit 3: Screen mode (0 = Normal, 1 = One screen)
　　　　Bits 4-7: Lower 4 bits of the mapper number (Mapper Number % 16)
    7:
　　　　Bits 0-3: Unused
　　　　Bits 4-7: Higher 4 bits of the mapper number (Mapper Number / 16)

    8-15: Unused


--------
 Notes
--------

  Game Speed

    BioNES is designed to work in sync with the monitor refresh. As a result,
    the game speed depends on your monitor's refresh rate if your computer is
    fast enough to process emulation tasks.

    If BioNES is too fast on your computer, please take the following procedures
    before starting BioNES.
      (1) Open the Display control panel
      (2) Set the refresh rate under 640x480 to 60Hz
    The setting may not be valid on some video cards, in which case you must
    press [F2] to add delay.

    If BioNES is too slow, simply press [F3] to increase the frameskip rate.


  Higher 4 bits of the mapper number

    Some games floating around the net have corrupt headers. Such games often
    have garbage in Byte #7 of the header. If any game doesn't work, you should
    check this first.


  Namcot Games (Japanese games only)

    In order to enable save on games like "Kaiju Monogatari", please uncheck
    the "battery_backed" bit of the header. These games do not use usual SRAM.
    More recent games like "Megami Tensei 2", "Sangokushi 2" use usual
    battery-backed SRAM.


  Patched Games (Japanese games only)

    Many of the recent games from Irem, Namcot, Konami, Taito and Sunsoft
    are patched for Nesticle Mapper 4. Because Nesticle didn't support the
    custom mappers of these companies.
    Unfortunately, Nesticle does not even emulate mapper 4 correctly, and
    these patches sometimes take advantage of Nesticle's bugs.
    Such patched games do not work well on BioNES and fwNES.
    Use original ROM images!


-------------
 Disclaimers
-------------

    BioNES Copyright 1998 Shu Kondo
    BioNES is distributed as freeware. The author accepts no reward for it.
    It also means that the author is in no way responsible for any damage
    or losses resulting from the use of this software.
    Use it at your own risk!



Shu Kondo
silver-knight@geocities.co.jp

* The author cannot spare a lot of time for BioNES, so don't expect a reply
from the author.


shwag shwag shwag
fight for freedom
open it up.