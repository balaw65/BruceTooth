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


   def returnPairedDevices(self):

      # Find all devices that are paired:
      pairedDevices = []
      objMgr = ObjectManager()
      devices = objMgr.GetAddresses()
      for address in devices:
         if devices[address]['Paired']:
            pairedDevices.append(address)
      return pairedDevices
 
      


if __name__ == '__main__':

   devices    = Devices()
   devices.returnPairedDevices()


