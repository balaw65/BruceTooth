#include "mybluez.h"
#include <QDebug>
#include <QArrayData>
#include <QMap>

Mybluez::Mybluez(QObject * parent)
{
    /* KEEP THIS, IT WORKS FOR REMOVING AND ADDING A DEVICE: */
    m_aDevice = new OrgLocalDeviceChangeInterface("org.freedesktop.fwupd", "/", QDBusConnection::systemBus(),this);

    m_anIntrospection = new OrgBluezIntrospect("org.bluez.obex", "/", QDBusConnection::sessionBus(), this);

    m_managedObject  = new OrgBluezObjectManager("org.bluez.obex", "/", QDBusConnection::sessionBus(),this);


    /* Set up slots to notify when a device changes: */
    connect(m_aDevice,
            SIGNAL(Changed()), this,
            SLOT(changed()));
    connect(m_aDevice,
            SIGNAL(DeviceAdded(QMap<QString,QVariant>)), this,
            SLOT(deviceAdded(QMap<QString,QVariant>)));
    connect(m_aDevice,
            SIGNAL(DeviceChanged(QMap<QString,QVariant>)), this,
            SLOT(deviceChanged(QMap<QString,QVariant>)));
    connect(m_aDevice,
            SIGNAL(DeviceRemoved(QMap<QString,QVariant>)), this,
            SLOT(deviceRemoved(QMap<QString,QVariant>)));

}
Mybluez::~Mybluez()
{

}
QObject * Mybluez::resultsFromGetDevices(QDBusMessage message)
{
    qDebug() << "Devices Have Been Found: ";
    qDebug() << "Argument Size:" << message.arguments().size();
    if (message.arguments().size() == 1)
    {
        QVariant v = message.arguments().at(0);
        qDebug() << "Variant v type is:" << v.type();
        //QDBusArgument arg = v.type();
        //v.data();

    }

    return nullptr;
}
QObject * Mybluez::resultsFromGetDevices(QDBusReply<QList<QVariantMap>> reply)
{
    qDebug() << "From function " << __FUNCTION__ << "Devices Have Been Found: ";


    return nullptr;
}
QObject * Mybluez::resultsFromGetIntrospect(QDBusMessage message)
{
    qDebug() << "Introspection found: ";
    qDebug() << "Message is:" << message;
    return nullptr;
}
QObject * Mybluez::resultsFromGetIntrospect(QDBusReply<QString> reply)
{
    qDebug() << "From function " << __FUNCTION__ << "Devices Have Been Found: ";
    qDebug() << "Reply is:" << reply;


    return nullptr;
}

const char * Mybluez::errorFromGetDevices()
{
    qDebug() << "Error From Get Devices call: ";
    return nullptr;
}
void Mybluez::getDevices()
{
   //QList<QVariant> devices;
   //devices.clear();
   //args.append(QVariant("A TEST"));

    QList<QList<QMap<QString,QVariant>>> zaList = m_aDevice->GetDevices();
    qDebug() << "za list size: " << zaList.size();

#if 0
   QList<QMap<QString,QVariant>> results =  m_aDevice->GetDevices();

   qDebug() << "HERE ARE THE DEVICES:";
   for (int i = 0; i < results.size(); i++)
   {
       QMap<QString,QVariant> aMap = results.at(i);
       QMapIterator<QString,QVariant> it(aMap);
       while (it.hasNext())
       {
           it.next();
           qDebug() << it.key() << " --> " << it.value();
       }

   }
   qDebug() << results;

#endif
#if 0


















   //QDBusMessage results = m_aDevice->callWithArgumentList(QDBus::Block, "GetDevices", args);
   //QDBusReply<QMap<QString, QVariant>> rs = m_aDevice->call(QDBus::Block, "GetDevices");
//   QMap<QString, QVariant> rs = m_aDevice->callWithArgumentList(QDBus::Block, "GetDevices", args);


   QDBusReply<QVariant> reply = m_aDevice->call(QDBus::Block, "GetDevices", args);
   if (reply.isValid())
   {
       qDebug() << "YAY!  Reply is valid!";
   }
   else {
       qDebug() << "Ohh:  Reply is NOT valid size is:  "; // << reply.value().size();
   }


// // NOT WORKING:
// bool v = m_aDevice->callWithCallback("GetDevices",
//                                       args,
//                                       this,
//                                       SLOT(resultsFromGetDevices(QDBusReply<QList<QVariantMap<QString, QVariant>>>)));

  
   bool v = m_aDevice->callWithCallback("GetDevices", args, this, SLOT(resultsFromGetDevices(QDBusMessage)));


   //qDebug() << rs.value().first();


#if 0
   QMap<QString,QVariant> reply1 = m_aDevice->GetDevices();
   qDebug() << "Devices Found: ";
   foreach(QString value, reply1.keys())
   {
       qDebug() << value << "\t:\t" << reply1[value];
   }
   QMap<QString,QVariant> reply2 = m_aDevice->GetHistory();
   qDebug() << "History Found: ";
   foreach(QString value, reply2.keys())
   {
       qDebug() << value << "\t:\t" << reply2[value];
   }
#endif

#endif
}
void Mybluez::getManagedObjects()
{
    qDebug() << "Attempting to get managed objects map....";

    QDBusMessage  result = m_managedObject->GetManagedObjects();
    qDebug() << "QDBusMessage:  " << result;

#if 0
    qDebug() << "Argument count:  " << result.arguments().size();
    QDBusArgument v = result.arguments()[0].value<QDBusArgument>();
    QMap<QString,QVariantMap> m; //QMap<QString, QMap<QString, QVariant>>> m;
    m.clear();

    v.beginMap();
    while (!v.atEnd() )
    {
       QString key;
       QVariantMap value;
       v.beginMapEntry();
       qDebug() << "Key:  " << key << ", Value:  " << value;
       v >> key >> value;
       v.endMapEntry();
       m[key] = value;
    }
    v.endMap();

    QVariantMap   m;
    QVariantList  l;

    v.beginArray();
    while (!v.atEnd())
    {
        v >> m;
        l.append(m);
    }
    v.endArray();
    qDebug() << "Object count:  " << l.size();
#endif
//    managedObjectsMap = m_managedObject->GetManagedObjects();
//    qDebug() << managedObjectsMap;
}
void Mybluez::getIntrospectable()
{
   QList<QVariant> args;
   args.clear();

 //  bool v = m_anIntrospection->callWithCallback("Introspect", args, this, SLOT(resultsFromGetIntrospect(QDBusMessage)));

   QString reply = m_anIntrospection->Introspect();
   qDebug() << reply;

#if 0
   QDBusReply<QString> reply = m_anIntrospection->call("Introspect");
   if (reply.isValid())
   {
       qDebug() << "YAY!  Reply is valid!";
   }
   else
   {
       qDebug() << "Ohh:  Reply is NOT valid size is:  "; // << reply.value().size();
   }
#endif
}

void Mybluez::changed()
{
   qDebug() << __FILE__ << ":" << __FUNCTION__;
}
void Mybluez::deviceAdded(QMap<QString,QVariant> v0)
{
   qDebug() << __FILE__ << ":" << __FUNCTION__;

   qDebug() << "Device added:";
   foreach(QString value, v0.keys())
   {
       qDebug() << value << "\t:\t" << v0[value];
   }
}
void Mybluez::deviceChanged(QMap<QString,QVariant> v0)
{
   qDebug() << __FILE__ << "\t:\t" << __FUNCTION__;
   qDebug() << "Device changed:";
   foreach(QString value, v0.keys())
   {
       qDebug() << value << "\t:\t" << v0[value];
   }
}
void Mybluez::deviceRemoved(QMap<QString,QVariant> v0)
{
   qDebug() << __FILE__ << ":" << __FUNCTION__;
   qDebug() << "Device removed:";
   foreach(QString value, v0.keys())
   {
       qDebug() << value << "\t:\t" << v0[value];
   }

}
