on run eventArgs	
set displayName to (do shell script "system_profiler SPDisplaysDataType|grep -q 'Cinema Display';echo $?")
	if displayName is "0" then
        tell application "System Events" to set the autohide of the dock preferences to false
    else
	    tell application "System Events" to set the autohide of the dock preferences to true
	end if
end run
