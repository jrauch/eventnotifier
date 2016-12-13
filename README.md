# eventnotifier

Eventnotifier is a simple Python script that uses PyObjC to run arbitrary
scripts - currently Applescript or Python - on either NSNotificationCenter or
NSDistributedNotificationCenter events.

Documentation is available here:
https://developer.apple.com/reference/foundation/nsnotificationcenter

and here:

https://developer.apple.com/reference/foundation/nsdistributednotificationcenter

The more important information is the list of notifications available.  For
NSNotificationCenter, that's easy:
https://developer.apple.com/reference/foundation/nsnotification.name

For NSDistributedNotificationCenter, it's not so easy - so I've included a
small script (dn.py) that will watch for all NSDNC events, and print them out 
as it sees them.
