#!/usr/bin/env python3

import os
import sys
import time
import testclass

from testclass import TestClass
from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GLib
from devices import Devices

loop = GLib.MainLoop()
# sessionBus = SessionBus()

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
            <method name='Test'/>
            <method name='Quit'/>
            <signal name='NotifyAgent'>
               <arg type='i'/>
               <arg type='i'/>
            </signal>
        </interface>
      </node>
   """
   NotifyAgent = signal()

   def EchoString(self, s):
      """returns whatever is passed to it"""
      return s

   def GetPairedDevices(a):
      """returns all devices paired to the local interface"""
      print("Call to Get Paired Devices was made")
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
      session.NotifyAgent(5, os.getpid())
      loop.quit()

   def Test(self):
      print("Test Called")
      session.NotifyAgent(2, 0)
 

#  def RunLoop(self):
#     loop.run()

if __name__ == '__main__':
#  sessionBus = SessionBus()
#  session    = Session()
#  sessionBus.publish("org.law.pydbus.BruceTooth", session)
#  loop.run()



   for i in range(1,2):
      try:
         pid = os.fork()
         print("pid: %i" % pid)
         if pid != 0:
            sessionBus = SessionBus()
            session    = Session()
            sessionBus.publish("org.law.pydbus.BruceTooth", session)
            loop.run()
            print("DDDDDOOOOOONNNNNNNEEEEE WITH SESSION!!!!")
         else:
            time.sleep(1)
            test = TestClass()
            print("DDDDDOOOOOONNNNNNNEEEEE WITH AGENT!!!!!!")

      except OSError:
         sys.stderr.write("Could not create a child process\n")




