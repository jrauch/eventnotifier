from subprocess import check_output
    
unsetmute='osascript -e "set volume output muted false"'
if SETMUTE == True:
    check_output(unsetmute, shell=True)
    SETMUTE = False
