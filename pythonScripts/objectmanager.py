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

      for key in managedObjects.GetManagedObjects():
         print key

     
      



if __name__ == '__main__':
   mybluez    = MyBluez()


   mgtObjects = ObjectManager()
   mgtObjects.GetManagedObjects()
   mgtObjects.DisplayDBusReturnValue()
   # mgtObjects.ListDevices()





