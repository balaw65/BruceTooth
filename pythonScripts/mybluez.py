#!/usr/bin/env python3
import re


class MyBluez:

   global query
   numberOftapStops = 0
   inDictionary     = False
   inInteger        = False
   inList           = False
   inString         = False
   inBool           = False
   inLong           = False
   dickRootList     = {}


   def __init__(self):
      print "Init Called"
      self.numberOftapStops = 0

   def SetQuery(self, value):
      self.query = value

   def DisplayDBusReturnValue(self):
      print("\n\nHere are the values of query:")
      # print(self.query)
      self.tabStop = ""
      q = self.query
      if q is None:
         return
      elif type(q) is dict:
         # fill root:
         print ("Filling root: ")
         for key in q:
            self.dickRootList[key] = q[key]
            print("%s >> " % key)
         print
         print
         self.ParseDictionary(q)
      elif type(q) is list:
         self.ParseList(q)


   def ParseDictionary(self, entry):
      for key in entry:
         if key in self.dickRootList:
            self.numberOftapStops = 0
         elif self.numberOftapStops == 0:
            self.numberOftapStops = 1
         tabStopString = ""
         for tabStop in range(0, self.numberOftapStops):
            tabStopString += "\t"
         if type(entry[key]) is None:
            self.numberOftapStops = 0
            return
         elif type(entry[key]) is dict:
            print("%s%s" % (tabStopString, key))
            if not self.inDictionary:
               self.numberOftapStops += 1
               self.inDictionary = True
            self.ParseDictionary(entry[key])
         elif type(entry[key]) is int:
            if not self.inInteger:
               self.numberOftapStops += 1
               self.inInteger = True
            self.ParseInteger(key, entry[key])
         elif type(entry[key]) is long:
            if not self.inLong:
               self.numberOftapStops += 1
               self.inLong = True
            self.ParseLong(key, entry[key])
         elif type(entry[key]) is bool:
            if not self.inBool:
               self.numberOftapStops += 1
               self.inBool = True
            self.ParseBool(key, entry[key])
         elif type(entry[key]) is list:
            if not self.inList:
               self.numberOftapStops += 1
               self.inList = True
            self.ParseList(entry[key])
         elif type(entry[key]) is str:
            if not self.inString:
               self.numberOftapStops += 1
               self.inString = True;
            self.ParseString(key, entry[key])
         else:
            self.numberOftapStops = 0
            print type(entry[key])
            return

   def ParseList(self, zaList):
      tabStopString = ""
      for tabStop in range(0, self.numberOftapStops):
         tabStopString += "\t"
 
      for value in zaList:
         # print("type value is a %s" % type(value))
         print ("%s%s" % (tabStopString, str(value)))
      self.numberOftapStops = 1

   def ParseInteger(self, key, value):
      tabStopString = ""
      for tabStop in range(0, self.numberOftapStops):
         tabStopString += "\t"
      print ("%s%s = %i" % (tabStopString, key, value))

   def ParseString(self, key, value):
      tabStopString = ""
      for tabStop in range(0, self.numberOftapStops):
         tabStopString += "\t"
      print ("%s%s = %s" % (tabStopString, key, value))

   def ParseBool(self, key, value):
      tabStopString = ""
      for tabStop in range(0, self.numberOftapStops):
         tabStopString += "\t"
      if value:
         print ("%s%s = TRUE" % (tabStopString, key))
      else:
         print ("%s%s = FALSE" % (tabStopString, key))
 
   def ParseLong(self, key, value):
      tabStopString = ""
      for tabStop in range(0, self.numberOftapStops):
         tabStopString += "\t"
      if value:
         print ("%s%s = 0x%x" % (tabStopString, key, value))
      else:
         print ("%s%s = 0x%x" % (tabStopString, key, value))
 


   # print("type entry[key] is a %s" % type(entry[key]))
   #def ParseList(self, entry):





if __name__ == '__main__':
   mybluez = MyBluez()





