#!/usr/bin/env python3

from subprocess import check_output
    
getmute='osascript -e "output muted of (get volume settings)"'
setmute='osascript -e "set volume output muted true"'

o = check_output(getmute, shell=True)
global SETMUTE
SETMUTE = False
if 'false' in o:
        check_output(setmute, shell=True)
        SETMUTE = True
