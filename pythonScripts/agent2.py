#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject

import sys
import dbus
import dbus.service
import dbus.mainloop.glib
from optparse import OptionParser
# import bluez



BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"




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


















class Agent2:

   def __init__(self):

      dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

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
      agent = Agent(bus, path)

      # mainloop = GObject.MainLoop()

      obj = bus.get_object(BUS_NAME, "/org/bluez");
      manager = dbus.Interface(obj, "org.bluez.AgentManager1")
      manager.RegisterAgent(path, capability)

      print("Agent is registered")


