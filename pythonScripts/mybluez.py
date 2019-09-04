#!/usr/bin/env python3
import re


class MyBluez:

   global query
   numberOftapStops = 0
   masterDick = {}


   def __init__(self):
      print "Init Called"
      self.numberOftapStops = 0

   def SetQuery(self, value):
      self.query = value

   def DisplayDBusReturnValue(self):
      print("\n\nHere are the values of query:")
      print(self.query)
      print("\n\n")
      self.tabStop = ""
      q = self.query
      if q is None:
         return
      elif type(q) is dict:
         self.ParseDictNew(q)
      elif type(q) is list:
         self.ParseListNew(q)



   def ParseListNew(self, value):
      for item in value:
         if type(item) is None:
            return
         elif type(item) is dict:
            self.ParseDictNew(item)
         elif type(item) is list:
            self.ParseListNew(item)
         else:
            print item


   def ParseDictNew(self, value):
      for key in value:
         # A way, perhaps not the best, do 
         # seperate array entries:
         if key in self.masterDick:
            print
            self.masterDick.clear()
         print ("[%s] ==> " % (key)),
         self.masterDick[key] = value
         if type(value[key]) is None:
            return
         elif type(value[key]) is list:
            self.ParseListNew(value[key])
         elif type(value[key]) is dict:
            self.ParseDictNew(value[key])
         else:
            print value[key]
 






if __name__ == '__main__':
   mybluez = MyBluez()





