#!/usr/bin/env python3
import dbus
import os
import time
from xml.etree import ElementTree

def findPaths(service,object_path):
   # print "   ",
   # print(object_path)
   if object_path == '/org/bluez/agent':
      print "FOUND!!!"
      print service
      os.exit(0)

   xml_string = ""
   try:
      obj = dbus.SystemBus().get_object(service, object_path)
      iface = dbus.Interface(obj, 'org.freedesktop.DBus.Introspectable')
      xml_string = iface.Introspect()
   except:
      print "unknown error"
      return

   for child in ElementTree.fromstring(xml_string):
      if child.tag == 'node':
         if object_path == '/':
            object_path =''
         new_path = '/'.join((object_path,child.attrib['name']))
         findPaths(service, new_path)

def isPath(service,object_path):
   obj = dbus.SystemBus().get_object(service, object_path)
   iface = dbus.Interface(obj, 'org.bluez.Agent1')
   xml_string = iface.Introspect()
   print xml_string    

print("System Bus: ")
bus = dbus.SystemBus()

"""
for i in range(1,100):
   isPath('org.bluez','/org/bluez/agent')
   print "\n\n\n"
   time.sleep(1) 

"""
for service in dbus.SystemBus().list_names():
   for i in range(1,100):
      findPaths(service, "/")

print("\nSession Bus: ")
for service in dbus.SessionBus().list_names():
   if service == "org.freedesktop.DBus":
      print(service)




