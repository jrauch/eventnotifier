import time

from Foundation import NSObject, NSAppleScript, NSBundle, NSDistributedNotificationCenter

from AppKit import NSWorkspace, NSWorkspaceDidWakeNotification, NSWorkspaceDidLaunchApplicationNotification, NSWorkspaceDidTerminateApplicationNotification
from PyObjCTools import AppHelper

class NotificationHandler(NSObject):
	def handler_(self, aNotification):
		print aNotification.name()
		return

dnc = NSDistributedNotificationCenter.defaultCenter()
no = NotificationHandler.new()

dnc.addObserver_selector_name_object_(no, "handler:", None, None)
AppHelper.runConsoleEventLoop()

