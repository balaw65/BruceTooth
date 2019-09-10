


from __future__ import absolute_import, print_function, unicode_literals

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

import sys
import dbus
import dbus.service
import time
import psutil
from optparse import OptionParser

from gi.repository import GLib


loop = GLib.MainLoop()
dbus_filter = "/org/law/pydbus/BruceTooth"
bus = SessionBus()




class TestClass:

   def __init__(self):
      print("TODO:  SUBSCRIBE TO SESSION FOR SIGNALS...")
      DBusGMainLoop(set_as_default=True)
      print("GOT HERE!!!!!!!!!!!!!!!!!!")
 
      # bus.subscribe(object = dbus_filter, signal_fired=self.SignalReceived);
      dbus.SessionBus().add_signal_receiver(self.SignalReceived, dbus_interface='org.law.pydbus.BruceTooth', signal_name='NotifyAgent')
      loop.run()

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
         print("Pid of session: %i" % c)
         for i in range(1,5):
            if psutil.pid_exists(c):
               print("Session is still running")
            else:
               print("Session is not running")
            print("Quiting agent in %i seconds" % (5-i))  
            time.sleep(1)
         if psutil.pid_exists(c):
            print("This is bad, session never ended")
         loop.quit()


