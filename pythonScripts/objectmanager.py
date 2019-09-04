#!/usr/bin/env python3
from mybluez import MyBluez
from pydbus import SystemBus
import dbus
import re


class ObjectManager(MyBluez):

   interfaceName   = "org.freedesktop.DBus.ObjectManager"
   busName         = "org.bluez"
   path            = "/"
   bus             = SystemBus()
   objectsListArray = []

   def __init__(self):
      print "Object Manager's Init Called"

        
   def GetManagedObjects(self):
      # Get devices is an Array of [Dict of [String,Variant]]:
      managedObjects = self.bus.get(self.busName, self.path)

      self.SetQuery(managedObjects.GetManagedObjects())

   def DoesDeviceExist(self, btNumber, deviceAddress):
      print("looking for device:  %s " % deviceAddress)
      managedObjects = self.bus.get(self.busName, self.path)

      # Look in keys for key called /org/bluez/hci<btNumber>/dev_<deviceAddress
      qpath = ("/org/bluez/hci%i/dev_%s" % (btNumber, deviceAddress)).replace(':','_')
      print("looking for path:  %s " % qpath)
 
      if qpath in managedObjects.GetManagedObjects():
         return qpath
      else:
         return None

   def ListDevices(self):
      managedObjects = self.bus.get(self.busName, self.path)
      devicesDick = managedObjects.GetManagedObjects()

      for key in devicesDick:
         print key
               
   def GetAddresses(self):
      managedObjects = self.bus.get(self.busName, self.path)
      devicesDick = managedObjects.GetManagedObjects()
      devices = {}
      # addresses = []

      for key in devicesDick:
         if len(key.split('/')) == 5:
            if key.find('/org/bluez/hci0/dev_') != -1:
               # addresses.append(devicesDick[key]['org.bluez.Device1']['Address'])
               addressKey = devicesDick[key]['org.bluez.Device1']['Address']
               devices[addressKey]  = devicesDick[key]['org.bluez.Device1']

      return devices
               


     
      



if __name__ == '__main__':
   mybluez    = MyBluez()


   mgtObjects = ObjectManager()
   mgtObjects.GetManagedObjects()
   mgtObjects.DisplayDBusReturnValue()
   print "\n\nLIST OF REGISTERED DEVICES DEVICES:"
   mgtObjects.ListDevices()





