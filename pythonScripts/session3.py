#!/usr/bin/env python3

import os, subprocess
import sys
import time
import threading

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
            <method name='MessageHost'>
               <arg type='s' name='s' direction='in'/>
            </method>
            <signal name='NotifyAgent'>
               <arg type='i'/>
               <arg type='i'/>
            </signal>
            <signal name='NotifyHost'>
                <arg type='i'/>
            </signal>
        </interface>
      </node>
   """
   NotifyAgent = signal()
   NotifyHost  = signal()


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
 

      devices = Devices()
      devices.pairDevice(s)

      pairedDevices = devices.returnPairedDevices()
      for d in pairedDevices:
         if d == s:
            print ("Device Paired")
            session.NotifyHost(1)
            return

      print ("Problem pairing device")
      session.NotifyHost(-1) 
 

   def RunAgent(self):
      print("Run Agent Called")
 
      # spawn agent (shell=True makes it non-blocking, i think):
      # Non-Blocking, use POpen
      try:
         # Test verions: results = subprocess.call(['python', 'agent3.py'], shell=False)
         subprocess.Popen(['python', 'agent.py'], shell=False)
 
         print("From session, run agent called"),
      except OSError:
         sys.stderr.write("OSError spawning agent\n");
         sys.exit(-1)
      except:
         sys.stderr.write("Error spawning agent\n");
         sys.exit(-1)

      # Verify agent is indeed running:
      bus = dbus.SystemBus()
      obj = bus.get_object('org.bluez', "/org/bluez");
      manager = dbus.Interface(obj, "org.bluez.AgentManager1")
      manager.RegisterAgent('/test/agent', "") #capability)

      # This should give me an error:

      time.sleep(2)
      try:
         manager.RegisterAgent('/test/agent', "") #capability)
      except dbus.DBusException as e:
         print
         print("|%s|" % e.message)
         if e.message != 'Already Exists':
            print ("Unexpected error:"),
            traceback.print_exc()
            print ("BAILING.....")
            sys.exit(-1)
      else:
         print ("Agent may already be registered")
         print ("BAILING.....")
         sys.exit(-1)
 


      # Agent hopefully is now running, notify host:
      session.NotifyHost(5)
 
      print("FROM SESSION RUNAGENT, AGENT CALLED!!!")

   def KillAgent(self):
      print("Kill Agent Called")
      # spawn agent:
      session.NotifyAgent(5, 0)
 
   def Test(self):
      print("Test Called")
      # spawn agent:
      # session.NotifyAgent(2, 0)
      session.NotifyHost(5)
 
   def Quit(self):
      """removes this object from the DBUS connection and exits"""
      print("Session quit called")
      session.NotifyAgent(5, os.getpid())
      loop.quit()

   def MessageHost(self, s):
      print ("A message to host needs to be sent:  "),
      print (s)
 
   def AgentThread(self):
      print("Spawning agent in session thread:")
      try:
         # Test verions: results = subprocess.call(['python', 'agent3.py'], shell=False)
         results = subprocess.call(['python', 'agent.py'], shell=False)
      except OSError:
         sys.stderr.write("OSError spawning agent\n");
      except:
         sys.stderr.write("Error spawning agent\n");
      print("Result from agent:  %i" % results)





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

