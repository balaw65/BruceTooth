#!/usr/bin/env python3

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GLib
from devices import Devices


loop = GLib.MainLoop()


sessionBus = SessionBus()


class Session(object):

   """
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
            <property name="SomeProperty" type="s" access="readwrite">
               <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
         </interface>
      </node>
   """

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

   def SomeProperty(self):
      return self._someProperty

   def Quit(self):
      """removes this object from the DBUS connection and exits"""
      print("Session quit called")
      loop.quit()

   def RunLoop(self):
      loop.run()

'''
if __name__ == '__main__':
   sessionBus = SessionBus()
   sessionBus.publish("org.law.pydbus.BruceTooth", Session())
   loop.run()
'''



