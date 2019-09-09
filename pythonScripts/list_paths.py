#!/usr/bin/env python3
import dbus


class ListPaths:


   def __init__(self):
      print "Init Called"

   def GetIntrospect(self):
      obj = dbus.SystemBus().get_object("org.bluez","/org/bluez/agent")
      iface = dbus.Interface(obj, "org.freedesktop.DBus.Introspectable")
      # iface = dbus.Interface(obj, "org.bluez.Agent1")
      print iface.Introspect()


if __name__ == '__main__':
   li = ListPaths()
   li.GetIntrospect()





