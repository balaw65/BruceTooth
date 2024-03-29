#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject

import sys
import dbus
import dbus.service
import dbus.mainloop.glib
import logging
import threading
import time
import traceback

from pydbus import SessionBus
from pydbus.generic import signal
from devices import Devices

from optparse import OptionParser
# import bluez

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

bus = None
device_obj = None
dev_path = None


msg_host = None

def ExitLoopThread():
   time.sleep(1)
   mainloop.quit()

def MessageHostThread(message):
   obj=dbus.SessionBus().get_object("org.law.pydbus.BruceTooth","/org/law/pydbus/BruceTooth")
   iface = dbus.Interface(obj,"org.law.pydbus.BruceTooth")
   iface.MessageHost(message)


 
def ask(prompt):
   '''
   obj=dbus.SessionBus().get_object("org.law.pydbus.BruceTooth","/org/law/pydbus/BruceTooth")
   iface = dbus.Interface(obj,"org.law.pydbus.BruceTooth")
   iface.MessageHost(prompt)
   ''' 
   x = threading.Thread(target=ExitLoopThread)
   x.start()
   try:
      return raw_input(prompt)
   except:
      return input(prompt)

def set_trusted(path): 
   props = dbus.Interface(bus.get_object("org.bluez", path),"org.freedesktop.DBus.Properties")
   props.Set("org.bluez.Device1", "Trusted", True)
   print("FROM AGENT:  Device at %s has been set to trusted" % path)

def dev_connect(path):
   dev = dbus.Interface(bus.get_object("org.bluez", path),"org.bluez.Device1")
   dev.Connect()
   print("FROM AGENT:  Device at %s has been set connected" % path)



class Rejected(dbus.DBusException):
   _dbus_error_name = "org.bluez.Error.Rejected"


class Agent(dbus.service.Object):
   """
      <node>
         <interface name='org.law.pydbus.BruceAgent'>
           <method name='AgentToMessageHost'>
               <arg type='s' name='s' direction='in'/>
            </method>
            <method name='HostToAgentMessage'>
               <arg type='s' name='s' direction='in'/>
            </method>
            <signal name='AgentToNotifyHost'>
                <arg type='i'/>
                <arg type='s'/>
            </signal>
        </interface>
      </node>
   """

   AgentToNotifyHost = signal()
   m_device = None
   m_Passkey = None
 
   exit_on_release = True

   def AgentToMessageHost(self, s):
      print ("A message came in from agent and needs to be sent to the host:"),
      print (s)
 
   def HostToAgentMessage(self, s):
      print ("A message came in from the host:  "),
      print (s)
      if self.m_device != None:
         if s == 'YES':
            set_trusted(self.m_device)

            pairedDeviceAddress = dbus.String(Devices().returnFirstPairedDevice())

            print(">>>>> PAIRED DEVICE IS TYPE:  "),
            print(type(pairedDeviceAddress))
            print(pairedDeviceAddress)

            agent.AgentToNotifyHost(2, "CC:44:63:20:D0:5F")

            #  FIXME: WHY IS THIS NOT WORKING??? dbus.String(pariredDeviceAddress)) #
            #agent.AgentToNotifyHost(2, dbus.String(pariredDeviceAddress))

            # No Longer need agent, call exit thread:
            x = threading.Thread(target=ExitLoopThread)
            x.start()
 
            return
         else:
            msg = "Pairing failed"
            agent.AgentToNotifyHost(-1, msg)
            raise Rejected("Device Rejected")
      else:
         msg = "Pairing failed"
         agent.AgentToNotifyHost(-1, msg)
         raise Rejected("Device Rejected")
 
   def set_exit_on_release(self, exit_on_release):
      self.exit_on_release = exit_on_release


   @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
   def Release(self):
      print("FROM AGENT:  Release")
      if self.exit_on_release:
         mainloop.quit()

   @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
   def AuthorizeService(self, device, uuid):
      print("FROM AGENT:  AuthorizeService (%s, %s)" % (device, uuid))
      authorize = ask("FROM AGENT:  Authorize connection (yes/no): ")
      if (authorize == "yes"):
         return
      raise Rejected("FROM AGENT:  Connection rejected by user")

   @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
   def RequestPinCode(self, device):
      print("FROM AGENT:  RequestPinCode (%s)" % (device))
      set_trusted(device)
      return ask("FROM AGENT:  Enter PIN Code: ")

   @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
   def RequestPasskey(self, device):
      print("FROM AGENT:  RequestPasskey (%s)" % (device))
      set_trusted(device)
      passkey = ask("FROM AGENT:  Enter passkey: ")
      return dbus.UInt32(passkey)

   @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
   def DisplayPasskey(self, device, passkey, entered):
      print("FROM AGENT:  DisplayPasskey (%s, %06u entered %u)" % (device, passkey, entered))

   @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
   def DisplayPinCode(self, device, pincode):
      print("FROM AGENT:  DisplayPinCode (%s, %s)" % (device, pincode))

   @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
   def RequestConfirmation(self, device, passkey):
      self.m_device  = device
      self.m_Passkey = passkey

      msg = "Confirm passkey %i" % passkey
      agent.AgentToNotifyHost(1, msg)

   @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
   def RequestAuthorization(self, device):
      print("FROM AGENT:  RequestAuthorization (%s)" % (device))
      auth = ask("Authorize? (yes/no): ")
      if (auth == "yes"):
         return
      raise Rejected("FROM AGENT:  Pairing rejected")

   @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
   def Cancel(self):
      print("FROM AGENT:  Cancel")

   def SignalReceived(a,b,c):

      print("a:", a)
      print("b:", b)
      print("c:", c)

      if   b == 1:
         if c == 1:
            msg_host = 'YES'
         else:
            msg_host = 'NO'
         
      elif b == 2:
         print("FROM AGENT:  Test Button Pressed")
         obj=dbus.SessionBus().get_object("org.law.pydbus.BruceTooth","/org/law/pydbus/BruceTooth")
         iface = dbus.Interface(obj,"org.law.pydbus.BruceTooth")
         iface.MessageHost("This is a test")
 
      elif b == 5:
         print("FROM AGENT:  Quitting Agent")
         obj = bus.get_object(BUS_NAME, "/org/bluez");
         manager = dbus.Interface(obj, "org.bluez.AgentManager1")
         manager.UnregisterAgent(path)


         mainloop.quit()

def pair_reply():
   print("FROM AGENT:  Device paired")
   set_trusted(dev_path)
   dev_connect(dev_path)
   mainloop.quit()

def pair_error(error):
   err_name = error.get_dbus_name()
   if err_name == "org.freedesktop.DBus.Error.NoReply" and device_obj:
      print("FROM AGENT:  Timed out. Cancelling pairing")
      device_obj.CancelPairing()
   else:
      print("FROM AGENT:  Creating device failed: %s" % (error))
   mainloop.quit()

if __name__ == '__main__':
   dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


   bus = dbus.SystemBus()


   # What the fuck does this do????
   capability = "KeyboardDisplay"

   parser = OptionParser()
   parser.add_option("-i", "--adapter",action="store",type="string",dest="adapter_pattern",default=None)
   parser.add_option("-c", "--capability", action="store",type="string", dest="capability")
   parser.add_option("-t", "--timeout", action="store",type="int", dest="timeout",default=60000)
   (options, args) = parser.parse_args()
   if options.capability:
      capability  = options.capability


   path = "/test/agent"
   pathOfBlueToothControl = "/org/bluez/agent"
   agent = Agent(bus, path)
   SessionBus().publish("org.law.pydbus.BruceAgent", agent)

   dbus.SessionBus().add_signal_receiver(agent.SignalReceived, dbus_interface='org.law.pydbus.BruceTooth', signal_name='NotifyAgent')

   mainloop = GObject.MainLoop()

   obj = bus.get_object(BUS_NAME, "/org/bluez");
   manager = dbus.Interface(obj, "org.bluez.AgentManager1")


   try:
      manager.UnregisterAgent(pathOfBlueToothControl)
   except:
      print("/org/agent1 not registered") 

   try:
      manager.UnregisterAgent(path)
   except:
      print("/org/test not registered") 

   manager.RegisterAgent(path, "") #capability)
   manager.RequestDefaultAgent(path)

   print("Agent is registered")
   mainloop.run()

   print("AGENT DONE")
 

