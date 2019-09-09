#!/usr/bin/env python3

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GLib
from devices import Devices
from agent3 import Agent3


loop = GLib.MainLoop()
# agent3 = None

sessionBus = SessionBus()


class Session(object):
   """
   Session definition.
   Emit / Publish a signal that is emitted when a request is made to quit python
   type='i' for integer.
   """
   dbus = """
      <node>
         <interface name='org.law.pydbus.BruceTooth'>
            <method name='EchoString'>
               <arg type='s' name='a' direction='in'/>
               <arg type='s' name='response' direction='out'/>
            </method>
            <method name='GetPairedDevices'>
               <arg type='as' name='response' direction='out'/>
            </method>
            <method name='PairDevice'>
               <arg type='s' name='s' direction='in'/>
            </method>
            <method name='Quit'/>
            <signal name="send_quit">
               <arg type='i'/>
            </signal>
        </interface>
      </node>
   """
   send_quit = signal()

   def EchoString(self, s):
      """returns whatever is passed to it"""
      return s

   def GetPairedDevices(a):
      """returns all devices paired to the local interface"""
      devices = Devices()
      a = devices.returnPairedDevices()

      for pDevice in a:
         print pDevice

      return a

   def PairDevice(self, s):
      print ("Attempting to pair device at address: %s" % s)
      devices = Devices()
      devices.pairDevice(s)

   def Quit(self):
      """removes this object from the DBUS connection and exits"""
      print("Session quit called")
      session.send_quit(1)
      loop.quit()

   def RunLoop(self):
      loop.run()

   def SetAgent3(self, a3):
      agent3 = a3

if __name__ == '__main__':
   sessionBus = SessionBus()
   session    = Session()
   sessionBus.publish("org.law.pydbus.BruceTooth", session)
   loop.run()


