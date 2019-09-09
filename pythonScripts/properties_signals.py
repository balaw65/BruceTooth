#!/usr/bin/env python3
import sys
import traceback
import dbus
import dbus.service
import dbus.glib

import gi
from gi.repository import GObject

class PropertySignals(dbus.service.Object):

   loop = None

   def __init__(self, bus_name, object_path, loop):
      dbus.service.Object.__init__(self, bus_name, object_path)
      self.loop = loop


def propertiesChanged(s, d, a):
   print "Signal Caught: Properties Changed"

   if type(s) is dbus.String:
      print "Arg(1): %s" % s
   else:
      print "Arg(1): Is an unexpected type"

   if type(d) is dbus.Dictionary:
      print "Arg(2):"
      for e in d:
         print "\t",
         print e,
         print " ===> ",
         if type(d[e]) is dbus.Array:
            print
            for element in d[e]:
               print "\t\t",
               print element
         elif type(d[e]) is dbus.Dictionary:
            print
            for f in d[e]:
               print "\t\t",
               print f,
               print " ===> ",
               print d[e][f]
         else:
            print d[e]
   else:
      print "Arg(2): Is an unexpected type"


   if type(a) is dbus.Array:
      print "Arg(3):"
      for element in a:
         print "\t",
         print element
   else:
      print "Arg(3): Is an unexpected type"
   print "------------------------------"
   print
   print

loop = GObject.MainLoop()
bus = dbus.SystemBus()
bus_name = dbus.service.BusName('org.bluez', bus=bus)
obj = PropertySignals(bus_name,'/org/bluez/hci0',loop)

bus.add_signal_receiver(propertiesChanged, dbus_interface='org.freedesktop.DBus.Properties',signal_name='PropertiesChanged')


loop.run()




