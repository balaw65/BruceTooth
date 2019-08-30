#!/usr/bin/env python3
from mybluez import MyBluez
from pydbus import SystemBus
import dbus
import re


class Properties(MyBluez):

   interfaceName   = "org.freedesktop.DBus.Properties"
   busName         = "org.bluez"
   path            = "/org/bluez/hci0"
   bus             = SystemBus()
   objectsListArray = []

   def __init__(self):
      print "Object Manager's Init Called"

        
   def PowerOff(self):
      properties = self.bus.get(self.busName, self.path)
      iface = "org.bluez.Adapter1"
      name  = "Powered"
      value = False
      properites.Set(iface, name, value)
 
   def PowerOn(self):
      properties = self.bus.get(self.busName, self.path)
      iface = "org.bluez.Adapter1"
      name  = "Powered"
      value = True
      properites.Set(iface, name, value)
     



if __name__ == '__main__':
   props    = Properties()
   props.PowerOff()
   props.PowerOn()






