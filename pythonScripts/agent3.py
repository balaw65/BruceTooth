
from __future__ import absolute_import, print_function, unicode_literals

from pydbus.generic import signal
from pydbus import SessionBus
from gi.repository import GObject

import sys
import dbus
import dbus.service
import dbus.mainloop.glib
from optparse import OptionParser

from gi.repository import GLib


loop = GLib.MainLoop()
dbus_filter = "/org/law/pydbus/BruceTooth"
bus = SessionBus()


class Agent3:

   def __init__(self):
      bus.subscribe(object = dbus_filter, signal_fired=SignalReceived);

   def RunLoop(self):
      print("starting loop (agent3)")
      loop.run()


   def Quit(self):
      print("ending loop (agent3)")
      loop.quit()


def SignalReceived(a,b,c,d,e):

   print("a:", a)
   print("b:", b)
   print("c:", c)
   print("d:", d)
   print("e:", e)
   print("Type of e is:  "),
   print(type(e))
   if e[0] == 5:
      print("Quitting Agent")
      loop.quit()




if __name__=="__main__":
   bus.subscribe(object = dbus_filter, signal_fired=SignalReceived);
   loop.run()



