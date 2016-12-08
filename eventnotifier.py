#!/usr/bin/env python

import time

from Foundation import NSObject, NSAppleScript, NSBundle, NSDistributedNotificationCenter

from AppKit import NSWorkspace, NSWorkspaceDidWakeNotification, NSWorkspaceDidLaunchApplicationNotification, NSWorkspaceDidTerminateApplicationNotification
from PyObjCTools import AppHelper

info = NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"

class NotificationHandler(NSObject):
    def setup(self, event, script, userinfokey=None, userinfomatch=None):
        super(NotificationHandler, self).__init__()
        self.event = event
        self.script = script
        self.userinfokey = userinfokey
        self.userinfomatch = userinfomatch
    
    def applescriptHandler_(self, aNotification):
        s = NSAppleScript.alloc().initWithSource_(self.script)
        s.executeAndReturnError_(None)
        return
        
    def pythonHandler_(self, aNotification):
        #print aNotification.userInfo()["NSApplicationBundleIdentifier"]
        print "triggered"
        if self.userinfokey == None or aNotification.userInfo()[self.userinfokey] == self.userinfomatch:
            print "YES"
            try:
                exec(self.script)
            except:
                print "error in script "+self.script
        return
        
    def shellHandler_(self, aNotification):
        print "Shell! " + self.script
        return


class DistributedNotificationHandler(NotificationHandler):
    pass

class NotificationManager():
    def __init__(self):
        self.notification_handlers = []
        self.ws = NSWorkspace.sharedWorkspace()
        self.nc = self.ws.notificationCenter()
        self.dnc = NSDistributedNotificationCenter.defaultCenter()
        
        return
        
    def register_handler(self, event, script_type, script, userinfokey=None, userinfomatch=None):
        nh = NotificationHandler.new()
        nh.setup(event, script, userinfokey, userinfomatch)
        self.notification_handlers.append(nh)
        
        self.nc.addObserver_selector_name_object_(
            self.notification_handlers[-1],
            script_type + "Handler:",
            event,
            None)
        return
    
    def register_distributed_handler(self, event, script_type, script, userinfokey=None, userinfomatch=None):
        nh = DistributedNotificationHandler.new()
        nh.setup(event, script, userinfokey, userinfomatch)
        self.notification_handlers.append(nh)
        
        self.dnc.addObserver_selector_name_object_(
            self.notification_handlers[-1],
            script_type + "Handler:",
            event,
            None)
        return

    def run(self):
        AppHelper.runConsoleEventLoop()

nm = NotificationManager()
nm.register_distributed_handler("com.apple.screenIsLocked", "python", '''
from subprocess import check_output

getmute='osascript -e "output muted of (get volume settings)"'
setmute='osascript -e "set volume output muted true"'

o = check_output(getmute, shell=True)

if 'false' in o:
        check_output(setmute, shell=True)
        global SETMUTE
        SETMUTE = True


''')
nm.register_distributed_handler("com.apple.screenIsUnlocked", "python", '''
from subprocess import check_output

unsetmute='osascript -e "set volume output muted false"'
if SETMUTE == True:
    check_output(unsetmute, shell=True)
    SETMUTE = False
''')
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
