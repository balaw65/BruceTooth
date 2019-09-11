#!/usr/bin/python


from __future__ import absolute_import, print_function, unicode_literals

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

import os
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import psutil
import xml.dom.minidom

from optparse import OptionParser
from gi.repository import GLib


loop = GLib.MainLoop()
dbus_filter = "/org/law/pydbus/BruceTooth"
bus = SessionBus()


BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

bus = None
device_obj = None
dev_path = None



def ask(prompt):
   try:
      return raw_input(prompt)
   except:
      return input(prompt)

def set_trusted(path): 
   props = dbus.Interface(bus.get_object("org.bluez", path),"org.freedesktop.DBus.Properties")
   props.Set("org.bluez.Device1", "Trusted", True)

def dev_connect(path):
   dev = dbus.Interface(bus.get_object("org.bluez", path),"org.bluez.Device1")
   dev.Connect()

class Rejected(dbus.DBusException):
   _dbus_error_name = "org.bluez.Error.Rejected"



class Agent(dbus.service.Object):
   exit_on_release = True

   def set_exit_on_release(self, exit_on_release):
      self.exit_on_release = exit_on_release


   @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
   def Release(self):
      print("Release")
      if self.exit_on_release:
         mainloop.quit()

   @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
   def AuthorizeService(self, device, uuid):
      print("AuthorizeService (%s, %s)" % (device, uuid))
      authorize = ask("Authorize connection (yes/no): ")
      if (authorize == "yes"):
         return
      raise Rejected("Connection rejected by user")

   @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
   def RequestPinCode(self, device):
      print("RequestPinCode (%s)" % (device))
      set_trusted(device)
      return ask("Enter PIN Code: ")

   @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
   def RequestPasskey(self, device):
      print("RequestPasskey (%s)" % (device))
      set_trusted(device)
      passkey = ask("Enter passkey: ")
      return dbus.UInt32(passkey)

   @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
   def DisplayPasskey(self, device, passkey, entered):
      print("DisplayPasskey (%s, %06u entered %u)" % (device, passkey, entered))

   @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
   def DisplayPinCode(self, device, pincode):
      print("DisplayPinCode (%s, %s)" % (device, pincode))

   @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
   def RequestConfirmation(self, device, passkey):
      print("RequestConfirmation (%s, %06d)" % (device, passkey))
      confirm = ask("Confirm passkey (yes/no): ")
      if (confirm == "yes"):
         set_trusted(device)
         return
      raise Rejected("Passkey doesn't match")

   @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
   def RequestAuthorization(self, device):
      print("RequestAuthorization (%s)" % (device))
      auth = ask("Authorize? (yes/no): ")
      if (auth == "yes"):
         return
      raise Rejected("Pairing rejected")

   @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
   def Cancel(self):
      print("Cancel")



   def TestFunction(self):
      print("This function is a test")


   def SignalReceived(a,b,c):

      print("a:", a)
      print("b:", b)
      print("c:", c)

      if   b == 2:
         print("Test Button Pressed")
      elif b == 5:
         print("Quitting Agent")
         loop.quit()
         return 0
def pair_reply():
   print("Device paired")
   set_trusted(dev_path)
   dev_connect(dev_path)
   loop.quit()

def pair_error(error):
   err_name = error.get_dbus_name()
   if err_name == "org.freedesktop.DBus.Error.NoReply" and device_obj:
      print("Timed out. Cancelling pairing")
      device_obj.CancelPairing()
   else:
      print("Creating device failed: %s" % (error))

   loop.quit()


if __name__ == '__main__':
   bus = dbus.SystemBus()

   capability = "KeyboardDisplay"

   parser = OptionParser()
   parser.add_option("-i", "--adapter",action="store",type="string",dest="adapter_pattern",default=None)
   parser.add_option("-c", "--capability", action="store",type="string", dest="capability")
   parser.add_option("-t", "--timeout", action="store",type="int", dest="timeout",default=60000)
   (options, args) = parser.parse_args()
   if options.capability:
      capability  = options.capability

   path = "/test/agent"
   # path = "/org/bluez/agent"
 
   test = Agent(bus, path)
   DBusGMainLoop(set_as_default=True)
 
   # bus.subscribe(object = dbus_filter, signal_fired=self.SignalReceived);
   dbus.SessionBus().add_signal_receiver(test.SignalReceived, dbus_interface='org.law.pydbus.BruceTooth', signal_name='NotifyAgent')


















   loop.run()
   print("TEST CLASS DONE (AKA AGENT)!!!")




