#!/usr/bin/env python3
from objectmanager import ObjectManager
from pydbus import SystemBus
from properties import Properties
import dbus
import re
import time


class BluezAdapter1:

   interfaceName   = "org.freedesktop.DBus.Properties"
   busName         = "org.bluez"
   path            = "/org/bluez/hci0"
   bus             = SystemBus()

   def __init__(self):
      print "Init Called"

        
   def RemoveDevice(self, deviceAddress):
      objMgr = ObjectManager()
      qpath = objMgr.DoesDeviceExist(0, deviceAddress)
      if qpath == None:
         print("Device at %s not found" % deviceAddress)
      else:
         print("Removing device at path:  %s" % qpath)
         adapter1 = self.bus.get(self.busName, self.path)
         adapter1.RemoveDevice(qpath)

         # Verify its gone:
         qpath = objMgr.DoesDeviceExist(0, deviceAddress)
         if qpath == None:
            print("Device Successfully removed")
         else:
            print("Unable to remove device")

   def ScanForDevices(self):
      props = Properties()

      # Power off:
      print "Powering off..."
      props.PowerOff()

      time.sleep(5)


      # Power on:
      print "Powering back on..."
      props.PowerOn()


      adapter1 = self.bus.get(self.busName, self.path)
      adapter1.StartDiscovery()
      for i in range(10,0,-1):
         print(i)
         time.sleep(1)

      # List devices:
      objMgr = ObjectManager()
      # objMgr.ListDevices()
      # List addresses:
      devices = objMgr.GetAddresses()
      for address in devices:
         print "%s\t%s" % (address, devices[address]['Name'])
      



if __name__ == '__main__':

   bluezAdapter1    = BluezAdapter1()
   # bluezAdapter1.RemoveDevice("00:06:66:C2:27:5C")
   bluezAdapter1.ScanForDevices()


