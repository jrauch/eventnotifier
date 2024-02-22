#!/usr/bin/osascript

tell application "System Events"
	try
		delay 10
		set _groups to groups of UI element 1 of scroll area 1 of group 1 of window "Notification Center" of application process "NotificationCenter"
		repeat with _group in _groups
			set _texts to value of static text 1 of _group
			set _actions to actions of _group
		
			if _texts contains "Disk Not Ejected" then
				repeat with _action in _actions
					if description of _action is in {"Close", "Clear All"} then
						perform _action
					end if
				end repeat
			end if
		end repeat
	end try
end tell
