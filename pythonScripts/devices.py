#!/usr/bin/env python3

from objectmanager import ObjectManager
from pydbus import SystemBus
from properties import Properties
import dbus
import re
import time


class Devices:

   interfaceName   = "org.freedesktop.DBus.Properties"
   busName         = "org.bluez"
   path            = "/org/bluez/hci0"
   bus             = SystemBus()


   def pairDevice(self, addressString):

      objMgr = ObjectManager()
      devices = objMgr.GetAddresses()

      newPath = objMgr.DoesDeviceExist(0, addressString)

      if newPath != None:
        print "Attempting to pair device at path: %s" % newPath
        device = self.bus.get(self.busName, newPath)
        device.Pair()
      else:
        print "Unable to find device at: %s" % addressString
 
   def returnPairedDevices(self):

      # Find all devices that are paired:
      pairedDevices = []
      objMgr = ObjectManager()
      devices = objMgr.GetAddresses()
      for address in devices:
         if devices[address]['Paired']:
            pairedDevices.append(address)
      return pairedDevices
 
   def returnFirstPairedDevice(self):

      # Find all devices that are paired:
      pairedDevices = []
      objMgr = ObjectManager()
      devices = objMgr.GetAddresses()
      for address in devices:
         if devices[address]['Paired']:
            return address
      return None 


if __name__ == '__main__':

   devices    = Devices()
   devices.returnPairedDevices()


