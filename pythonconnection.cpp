#include "pythonconnection.h"

#include "mainwindow.h"

#include <QDebug>
#include <QDBusReply>
#include <QtCore/QCoreApplication>

PythonConnection::PythonConnection(QObject * obj):QObject(obj)
{
   qDebug() << __FILE__ << ":" << __FUNCTION__;
   m_pairedDeviceAddressString = QString("");
}
PythonConnection::~PythonConnection()
{
   qDebug() << __FILE__ << ":" << __FUNCTION__;
}
void PythonConnection::setMainWindow(MainWindow * value)
{
   m_mainWindow = value;
}
MainWindow * PythonConnection::getMainWindow()
{
   return  m_mainWindow;
}

int  PythonConnection::connectInterface()
{
    m_iface = new QDBusInterface(SERVICE_NAME,  // Service
                                 "/org/law/pydbus/BruceTooth",           // Path
                                 "org.law.pydbus.BruceTooth",    // Interface
                                 QDBusConnection::sessionBus(),  // Bus
                                 this);
    if (!m_iface->isValid())
    {
        qDebug() << "Error connecting to python" << qPrintable(QDBusConnection::sessionBus().lastError().message());
        return -1;
    }
    qDebug() << "Connecting signal NotifyHost";
    connect(m_iface,SIGNAL(NotifyHost(int)),this,SLOT(notification(int)));
    return 0;
}
QString PythonConnection::getPairedDevices()
{
    //QVariantList

   QDBusReply<QStringList> reply = m_iface->call("GetPairedDevices");
   if (reply.isValid())
   {
       if (reply.value().length() != 1)
       {
           qDebug() << "Either zero or more than one device is paired...";
           return "UNDETERMINED";
       }


#if 0  //FIXME: Handle if there are multiple devices:
      foreach(QString v, reply.value())
      {
          lastOfList = v;
      }
#endif
      return reply.value().last();
   }
   else {
      qDebug() << "FUCK, REPLY IS NOT VALID";
   }
   return QString("");
}
void PythonConnection::notification(int v)
{
    qDebug() << "NOTIFICATION FROM PYTHON:  " << v;
    if (v == -1)
    {
        m_pairedDeviceAddressString = "ERROR";
        qWarning() << "AN ERROR WAS SENT FROM PYTHON";
    }
    else if (v == 1)
    {
        qDebug() << "DEVICE SUCCESSFULLY PAIRED";
        m_mainWindow->pairingSucceeded(m_pairedDeviceAddressString);
    }
    else if (v == 5)
    {
        if (m_pairedDeviceAddressString.length() > 0)
           m_iface->call("PairDevice", m_pairedDeviceAddressString);
    }
}
void PythonConnection::pairDevice(QString addressString)
{
    // start agent:
    m_iface->call("RunAgent");
    m_pairedDeviceAddressString = addressString;

    //m_iface->call("PairDevice", addressString);
}
void PythonConnection::startAgent()
{
    m_iface->call("RunAgent");
}
void PythonConnection::killAgent()
{
    m_iface->call("KillAgent");
}

void PythonConnection::quitPython()
{
    m_iface->call("Quit");
}
void PythonConnection::test()
{
    m_iface->call("Test");
}

#if 0
void PythonConnection::messageFromPython()
{
   qDebug() << __FILE__ << ":" << __FUNCTION__;
}
void PythonConnection::sendMessageToPython(const QString &query)
{
    qDebug() << __FILE__ << ":" << __FUNCTION__ << query;
}
#endif
