#!/usr/bin/env python3
from mybluez import MyBluez
from pydbus import SystemBus
import dbus
import re


class FWUPD(MyBluez):

   interfaceName   = "org.freedesktop.fwupd"
   sessionName     = "org.freedesktop.fwupd"
   path            = "/"
   bus             = SystemBus()
   deviceListArray = []

   def __init__(self):
      print "Init Called"

   def GetDevices(self):
      # Get devices is an Array of [Dict of [String,Variant]]:

      remote_object = self.bus.get(self.interfaceName, self.path)
      self.SetQuery(remote_object.GetDevices())
      self.DisplayDBusReturnValue()

   def ListDevices(self):
      print("\n\nHere are the list of devices:")
      for aDevice in self.deviceListArray:
         for key in aDevice:
            print("%s ==> %s" % (key, aDevice[key]))
         print("---------------")



if __name__ == '__main__':
   fwupd = FWUPD()
   fwupd.GetDevices()
   # fwupd.ListDevices()





