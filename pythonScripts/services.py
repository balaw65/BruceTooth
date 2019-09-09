import dbus

for service in dbus.SystemBus().list_names():
   print service,
   print " type ",
   print type(service)


