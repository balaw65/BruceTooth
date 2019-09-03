#!/usr/bin/env python3

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GLib
from devices import Devices
loop = GLib.MainLoop()
bus = SessionBus()


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


#     pairedDevices = devices.returnPairedDevices()

#     s = ""
#     if len(pairedDevices) > 0:
#        for pDevice in pairedDevices:
#           s += pDevice + '|'
#     else:
#        s = "None"

#     return s





   def SomeProperty(self):
      return self._someProperty

   def Quit(self):
      """removes this object from the DBUS connection and exits"""
      loop.quit()



bus = SessionBus()
bus.publish("org.law.pydbus.BruceTooth", Session())
loop.run()


