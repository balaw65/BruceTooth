#!/usr/bin/env python3
from mybluez import MyBluez
from gi.repository import GLib
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
      properties.Set(iface, name, GLib.Variant("b", False))
 
   def PowerOn(self):
      properties = self.bus.get(self.busName, self.path)
      iface = "org.bluez.Adapter1"
      name  = "Powered"
      properties.Set(iface, name, GLib.Variant("b", True))

   def GetAll(self):
      properties = self.bus.get(self.busName, self.pathIPhone)
      iface = "org.bluez.Adapter1"
      allProps = properties.GetAll(iface)
      print allProps
     



if __name__ == '__main__':
   props    = Properties()
   props.GetAll()
   # props.PowerOff()
   # props.PowerOn()






