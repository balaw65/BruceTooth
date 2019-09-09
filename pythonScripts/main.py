#!/usr/bin/python

from session import Session
from agent3 import Agent3
from pydbus import SessionBus


import sys
import os

from gi.repository import GLib



def agent():
   print("Agent process")
   print("DONE")
   
def session():
   print("Session process") 
   sess = Session()
   sessionBus = SessionBus()
   sessionBus.publish("org.law.pydbus.BruceTooth", sess)


   sess.RunLoop()
   print("DONE")

def forkHere():

#   session()

   try:
      pid = os.fork()
      if pid == 0:
         agent()
         print("PID IS ZERO")
      else:
         session()
   except OSError:
      sys.stderr.write("Could not create a child process\n")

forkHere()


''' 
forks = 3
if len(sys.argv) == 2:
    forks = int(sys.argv[1])
 
for i in range(forks):
    try:
        pid = os.fork()
    except OSError:
        sys.stderr.write("Could not create a child process\n")
        continue
 
    if pid == 0:
        print("In the child process {} that has the PID {}".format(i+1, os.getpid()))
        exit()
    else:
        print("In the parent process after forking the child {}".format(pid))
 
print("In the parent process after forking {} children".format(forks))
 
for i in range(forks):
    finished = os.waitpid(0, 0)
    print(finished)
''' 
