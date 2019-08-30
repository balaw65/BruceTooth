#!/usr/bin/env python3
from pydbus import SystemBus
import dbus
import re


class FWUPD:

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
      listOfDevices = {}
      listOfDevices = remote_object.GetDevices()
      for device in listOfDevices:
         deviceStrippedCurlyBrackets = re.search(r'{(.*?)}',str(device)).group(1)

         # Ignore commas within []
         deviceFindInnerBrackets = re.findall(r'\[(.*?)\]',str(deviceStrippedCurlyBrackets))

         i = 0
         for innerBracket in deviceFindInnerBrackets:
            deviceStrippedCurlyBrackets = deviceStrippedCurlyBrackets.replace(innerBracket, ("~r~~~~s%is~" % i))
            i += 1


         keyPairHash = re.split(r',\s+', deviceStrippedCurlyBrackets)
         entry = {}

         # Split by colon, add to tuple:
         for keyPair in keyPairHash:
            keyPairArray = re.split(r':\s+', keyPair)
            i = 0
            for innerBracket in deviceFindInnerBrackets:
               if keyPairArray[1].find("~r~~~~s%is~" % i):
                  keyPairArray[1] = keyPairArray[1].replace(("~r~~~~s%is~" % i), innerBracket)
                  i += 1
               
            entry[keyPairArray[0]] = keyPairArray[1]

         self.deviceListArray.append(entry)

   def ListDevices(self):
      print("\n\nHere are the list of devices:")
      for aDevice in self.deviceListArray:
         for key in aDevice:
            print("%s ==> %s" % (key, aDevice[key]))
         print("---------------")



if __name__ == '__main__':
   fwupd = FWUPD()
   fwupd.GetDevices()
   fwupd.ListDevices()





