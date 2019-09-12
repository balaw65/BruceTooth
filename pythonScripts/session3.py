#!/usr/bin/env python3

import os, subprocess
import sys
import time
import agent
import dbus
import xml.dom.minidom

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GLib
from devices import Devices
from xml.etree import ElementTree

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
            <method name='RunAgent'/>
            <method name='KillAgent'/>
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

   # This is not always being called, why not??? 
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
      # start agent:
      # spawn agent (shell=True makes it non-blocking, i think):
      subprocess.Popen('python agent.py', shell=True)
 
      devices = Devices()
      devices.pairDevice(s)

   def RunAgent(self):
      print("Run Agent Called")
      # spawn agent (shell=True makes it non-blocking, i think):
      subprocess.Popen('python agent.py', shell=True)
      print("FROM SESSION RUNAGENT, AGENT CALLED!!!")

   def KillAgent(self):
      print("Kill Agent Called")
      # spawn agent:
      session.NotifyAgent(5, 0)
 
   def Test(self):
      print("Test Called")
      # spawn agent:
      session.NotifyAgent(2, 0)
 
   def Quit(self):
      """removes this object from the DBUS connection and exits"""
      print("Session quit called")
      session.NotifyAgent(5, os.getpid())
      loop.quit()



#  def RunLoop(self):
#     loop.run()

if __name__ == '__main__':

   try:
      sessionBus = SessionBus()
      session    = Session()
      sessionBus.publish("org.law.pydbus.BruceTooth", session)

      # Verify session? 
      obj=dbus.SessionBus().get_object("org.law.pydbus.BruceTooth","/org/law/pydbus/BruceTooth")
      iface = dbus.Interface(obj,"org.freedesktop.DBus.Introspectable")
      
      doc = xml.dom.minidom.parseString(iface.Introspect())
      methods = doc.getElementsByTagName("method")
      sessionMethods = []
      for method in methods:
         if ((method.getAttribute("name") == 'GetPairedDevices') or
                  (method.getAttribute("name") == 'PairDevice') or
                        (method.getAttribute("name") == 'Test') or
                        (method.getAttribute("name") == 'Quit')):
            sessionMethods.append(method.getAttribute("name"))
      if len(sessionMethods) != 4:
         sys.stderr.write("Not all of the session methods were found\n")
         sys.stderr.write("Quiting session handler\n")
         os.exit(-1)

      loop.run()
   except OSError:
      sys.stderr.write("Could not create a child process\n")

