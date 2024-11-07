# fr_ng

An alternative configuration file for a French keyboard under Linux/XKB. The solution proposed here can also be used by those who simply want to create their own configuration; there's no need to know the rules for writing configuration files. Simply replace the symbols by others, launch the generation tool… Et voilà !

### Step 1: Generate and install the fr_ng file in /usr/share/X11/xkb/symbols...
`sudo ./install.sh`

### Step 2: In my case, I need to edit the Sway configuration file to specify my keyboard layout

     input type:keyboard {
           xkb_layout "fr_ng"
           xkb_variant "fr_ng01"
     }

Note: The generated file also contains the instructions used to generate it... 
Please see the initial "./fr_ng" file. This file contains additional information and a representation of the configured keyboard.
