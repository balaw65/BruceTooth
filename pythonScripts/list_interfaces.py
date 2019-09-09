#!/usr/bin/env python3
from pydbus import SystemBus
import dbus
import re


class ListInterfaces:

   busName         = "org.bluez"
   path            = "/org/bluez"
   bus             = SystemBus()
   deviceListArray = []

   def __init__(self):
      print "Init Called"

   def GetIntrospect(self):
      li = self.bus.get(self.busName, self.path)
      print li.Introspect()


if __name__ == '__main__':
   li = ListInterfaces()
   li.GetIntrospect()





