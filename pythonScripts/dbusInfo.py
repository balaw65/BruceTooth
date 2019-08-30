#!/usr/bin/env python3
import dbus

print("System Bus: ")
bus = dbus.SystemBus()
for service in dbus.SystemBus().list_names():
   object_path = "/org/freedesktop/DBus"
   if service == "org.freedesktop.DBus":
      print(service)
      obj = bus.get_object(service, object_path)
      print(obj)

print("\nSession Bus: ")
for service in dbus.SessionBus().list_names():
   if service == "org.freedesktop.DBus":
      print(service)


