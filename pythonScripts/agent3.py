#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject


import dbus
import dbus.service
import dbus.mainloop.glib
import logging
import threading
import time



from gi.repository import GLib



def ask(prompt):
   try:
      return raw_input(prompt)
   except:
      return input(prompt)


class Agent3:

   def CountDownThread(self):
      print("Killing agent in:")

      answer = ask("Begin countdown?")
      if (answer == "yes"):
         print("Yes recieved")
         for i in range(1,10):
            print("%i seconds" % (10 - i))
            time.sleep(1)
         mainloop.quit()
      else:
         print("No countdown, just leaving..")
         mainloop.quit()
      return 5
 



if __name__=="__main__":
   dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
   mainloop = GObject.MainLoop()


   print("Agent spawned, creating logger...")
   format = "%(asctime)s: %(message)s"
   logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

   agent = Agent3()

   x = threading.Thread(target=agent.CountDownThread)
   x.start()
   print("Count down thread started...")


   mainloop.run()



