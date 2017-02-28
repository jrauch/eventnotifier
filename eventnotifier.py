#!/usr/bin/env python

import time

from Foundation import NSObject, NSAppleScript, NSBundle, NSDistributedNotificationCenter

from AppKit import NSWorkspace, NSWorkspaceDidWakeNotification, NSWorkspaceDidLaunchApplicationNotification, NSWorkspaceDidTerminateApplicationNotification
from PyObjCTools import AppHelper

import os

info = NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"

class EventNotifier():
    def __init__(self, distributed_path, notification_path):
        self.distributed_path=distributed_path
        self.notification_path=notification_path
        self.notification_manager=NotificationManager()

    def run(self):
        self.load_configs(self.distributed_path, self.notification_manager.register_distributed_handler)
        self.load_configs(self.notification_path, self.notification_manager.register_handler)
        self.notification_manager.run()

    def load_configs(self, path, registration):
        try:
            notification_events = os.listdir(os.path.expanduser(path))
        except OSError:
            return
        
        for event in notification_events:
            event_path = os.path.expanduser(path)+"/"+event
            handlers = os.listdir(event_path)
            handlers = [ os.path.expanduser(event_path) + "/" + a for a in handlers]

            for handler in handlers:
                buffer = open(handler).read()
                file_extension = os.path.splitext(handler)[1][1:]
                #print event+" "+file_extension
                #print buffer
                registration(event, file_extension, buffer)


    def load_notification_configs(self):
        return

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
       
    def pyHandler_(self, aNotification):
        self.pythonHandler_(aNotification)

    def pythonHandler_(self, aNotification):
        #print aNotification.userInfo()["NSApplicationBundleIdentifier"]
        if self.userinfokey == None or aNotification.userInfo()[self.userinfokey] == self.userinfomatch:
            try:
                exec(self.script)
            except:
                print "error in script "+self.script
        return
    
    def shHandler_(self, aNotification):
        self.shellHandler(aNotification)

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


if __name__ == '__main__':
    en = EventNotifier("~/.events/dNotifications", "~/.events/Notifications")
    en.run()