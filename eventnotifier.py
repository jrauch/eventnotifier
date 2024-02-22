#!/usr/bin/env python3

import time

from Foundation import NSObject, NSAppleScript, NSBundle, NSDistributedNotificationCenter

from AppKit import NSWorkspace, NSWorkspaceDidWakeNotification, NSWorkspaceDidLaunchApplicationNotification, NSWorkspaceDidTerminateApplicationNotification
from PyObjCTools import AppHelper

import os
from subprocess import call

info = NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"

class EventNotifier():
    def __init__(self, distributed_path, notification_path):
        self.distributed_path=distributed_path
        self.notification_path=notification_path
        self.notification_manager=NotificationManager()

    def run(self):
        self.load_events(self.notification_path, self.notification_manager.register_handler)
        self.load_events(self.distributed_path, self.notification_manager.register_distributed_handler)

        self.notification_manager.run()

    def load_events(self, path, registration):
        try:
            notification_events = os.listdir(os.path.expanduser(path))
        except OSError:
            return

        for event in notification_events:
            event_path = os.path.expanduser(path) + "/" + event
            print(f"Registering event {event} at path {event_path}")
            registration(event, event_path)

class NotificationHandler():
    def __init__(self, event, path):
        self.event = event
        self.path = path

    def event_handler_(self, aNotification):
        for proc in self.get_script_paths():
            rval = call(proc)
            print(f"{proc} returned {rval}")

        return

    def get_script_paths(self):
        notification_event_scripts = os.listdir(self.path)
        notification_event_scripts = [self.path + "/" + x for x in notification_event_scripts]
        return notification_event_scripts

# why is there a seperate class for distbuted if it's just a pass?
# because eventually i'll have the ability to remove handlers and this
# will let me have a single list while being able to cancel different types without
# having to keep 2 lists.
class DistributedNotificationHandler(NotificationHandler):
    pass

class NotificationManager():
    def __init__(self):
        self.notification_handlers = []
        self.ws = NSWorkspace.sharedWorkspace()
        self.nc = self.ws.notificationCenter()
        self.dnc = NSDistributedNotificationCenter.defaultCenter()
        return
        
    def register_handler(self, event, path):
        nh = NotificationHandler(event, path)
        self.notification_handlers.append(nh)

        self.nc.addObserver_selector_name_object_(
            self.notification_handlers[-1],
            "event_handler:",
            event,
            None)
        return
    
    def register_distributed_handler(self, event, path):
        nh = DistributedNotificationHandler(event, path)
        self.notification_handlers.append(nh)
        
        self.dnc.addObserver_selector_name_object_(
            self.notification_handlers[-1],
            "event_handler:",
            event,
            None)
        return

    def run(self):
        AppHelper.runConsoleEventLoop()


if __name__ == '__main__':
    en = EventNotifier("~/.events/dNotifications", "~/.events/Notifications")
    en.run()
