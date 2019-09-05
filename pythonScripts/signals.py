#!/usr/bin/env python3
import sys
import traceback
import dbus
import dbus.service
import dbus.glib

import gi
from gi.repository import GObject

class Test(dbus.service.Object):

   loop = None

   def __init__(self, bus_name, object_path, loop):
      dbus.service.Object.__init__(self, bus_name, object_path)
      self.loop = loop

def DeviceAdded(*args, **kwargs):
   print "Signal Caught: Device Added"
   print args
   print kwargs

def DeviceRemoved(*args):
   print "Signal Caught: Device Removed"


def interfacesAdded(p, a):
   print "Signal Caught: Interfaces Added"
   print "p:",
   print p
   print "type a is: ",
   print type(a)
   if type(a) is dbus.Dictionary:
      for b in a:
         print "\ttype a[b] is: ",
         print type(a[b])
         if type(a[b]) is dbus.Dictionary:
            for c in a[b]:
               print "\t\ttype a[b][c] is: ",
               print type(a[b][c])
               if type(a[b][c]) is dbus.String:
                  print "\t\t\t",
                  print c,
                  print " ===> (string): ",
                  print a[b][c]
               elif type(a[b][c]) is dbus.Boolean:
                  print "\t\t\t",
                  print c,
                  print " ===> (boolean): ",
                  print a[b][c]
               elif type(a[b][c]) is dbus.ObjectPath:
                  print "\t\t\t",
                  print c,
                  print " ===> (object path): ",
                  print a[b][c]
               elif type(a[b][c]) is dbus.Int16:
                  print "\t\t\t",
                  print c,
                  print " ===> (int16_t): ",
                  print a[b][c]
               elif type(a[b][c]) is dbus.Int32:
                  print "\t\t\t",
                  print c,
                  print " ===> (int32_t): ",
                  print a[b][c]
               elif type(a[b][c]) is dbus.Dictionary:
                  for d in a[b][c]:
                     print "\t\t\t\ttype a[b][c][d] is: ",
                     print type(a[b][c][d])
                     if type(a[b][c][d]) is dbus.Dictionary:
                         for e in a[b][c][d]:
                            print "\t\t\t\t\t",
                            print e,
                            print " ===> ",
                            print a[b][c][d][e]
                     else:
                         print "\t\t\t\t",
                         print d,
                         print " ===> ",
                         print a[b][c][d]
               elif type(a[b][c]) is dbus.Array:
                  for d in a[b][c]:
                     print "\t\t\t\t",
                     print d
   

def interfacesRemoved(p, a):
   print "Signal Caught: Interfaces Removed"
   print "p:",
   print p
   print "a:",
   print a



loop = GObject.MainLoop()
bus = dbus.SystemBus()
bus_name = dbus.service.BusName('org.bluez', bus=bus)
obj = Test(bus_name,'/',loop)

# bus.add_signal_receiver(DeviceAdded, dbus_interface='org.freedesktop.fwupd',signal_name='DeviceAdded')
# bus.add_signal_receiver(DeviceRemoved, dbus_interface='org.freedesktop.fwupd',signal_name='DeviceAdded')
bus.add_signal_receiver(interfacesAdded, dbus_interface='org.freedesktop.DBus.ObjectManager',signal_name='InterfacesAdded')
bus.add_signal_receiver(interfacesRemoved, dbus_interface='org.freedesktop.DBus.ObjectManager',signal_name='InterfacesRemoved')


loop.run()




