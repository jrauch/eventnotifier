#!/usr/bin/env python

import time

from Foundation import NSObject, NSAppleScript, NSBundle

from AppKit import NSWorkspace, NSWorkspaceDidWakeNotification
from PyObjCTools import AppHelper

info = NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"

class NotificationHandler(NSObject):
    def setup(self, event, script):
        super(NotificationHandler, self).__init__()
        self.event = event
        self.script = script
    
    def applescriptHandler_(self, aNotification):
        s = NSAppleScript.alloc().initWithSource_(self.script)
        s.executeAndReturnError_(None)
        return
        
    def pythonHandler_(self, aNotification):
        print "Python! " + self.script
        return
        
    def shellHandler_(self, aNotification):
        print "Shell! " + self.script
        return

class NotificationManager():
    def __init__(self):
        self.notification_handlers = []
        self.ws = NSWorkspace.sharedWorkspace()
        self.nc = self.ws.notificationCenter()
        return
        
    def register_handler(self, event, script_type, script):
        nh = NotificationHandler.new()
        nh.setup(event, script)
        self.notification_handlers.append(nh)
        
        self.nc.addObserver_selector_name_object_(
            self.notification_handlers[-1],
            script_type + "Handler:",
            event,
            None)
        return
        
    def run(self):
        AppHelper.runConsoleEventLoop()

nm = NotificationManager()
nm.register_handler(NSWorkspaceDidWakeNotification, "applescript", '''
on run eventArgs	
	set displayName to (do shell script "system_profiler SPDisplaysDataType|grep -q 'Cinema Display';echo $?")
	if displayName is "0" then
		tell application "System Events" to set the autohide of the dock preferences to false
	else
		tell application "System Events" to set the autohide of the dock preferences to true
	end if
end run
''')
nm.run()
