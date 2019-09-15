#include "pythonconnection.h"

#include "mainwindow.h"

#include <QDebug>
#include <QDBusReply>
#include <QtCore/QCoreApplication>

PythonConnection::PythonConnection(QWidget *parent):QDialog(parent),ui(new Ui_PyMessage)
{
   ui->setupUi(this);
   this->hide();

   m_pairedDeviceAddressString = QString("");
   m_iface = nullptr;
   m_ifaceAgent = nullptr;

   ui->justOkButtonBox->hide();

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
                                 "/org/law/pydbus/BruceTooth",   // Path
                                 "org.law.pydbus.BruceTooth",    // Interface
                                 QDBusConnection::sessionBus(),  // Bus
                                 this);
    if (!m_iface->isValid())
    {
        qDebug() << "Error connecting to python" << qPrintable(QDBusConnection::sessionBus().lastError().message());
        return -1;
    }
    qDebug() << "Connecting signal NotifyHost";
    connect(m_iface,SIGNAL(NotifyHost(int, QString)),this,SLOT(notification(int, QString)));

    return 0;
}
QString PythonConnection::getPairedDevices()
{

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
void PythonConnection::notification(int v, QString message)
{
    qDebug() << "NOTIFICATION FROM PYTHON:  " << v;
    QList<QVariant> args;
    args.clear();

    switch (v)
    {
    case NOTIFICATION_ERROR:
        m_pairedDeviceAddressString = "ERROR";
        qWarning() << "AN ERROR WAS SENT FROM PYTHON";
        break;
    case PAIRED_SUCCESS:
        qDebug() << "DEVICE SUCCESSFULLY PAIRED";
        m_mainWindow->pairingSucceeded(m_pairedDeviceAddressString);
        break;
    case PASSKEY_MESSAGE:
        qDebug() << "MESSAGE FROM PYTHON IS:";
        qDebug() << message;
        ui->buttonBox->show();
        ui->justOkButtonBox->hide();
        ui->message->setText(message);
        this->show();
        break;
    case CONNECT_AGENT:
        ConnectAgent();
        args.append(m_pairedDeviceAddressString);

        /* Use call with callback so it's non-blocking */
        if (m_pairedDeviceAddressString.length() > 0)
           m_iface->callWithCallback("PairDevice",args,this, SLOT(ResponseFromPairing()));

        break;
    default:
        qDebug() << ">>>>>> RECIEVED UNKNOWN CMD FROM PYTHON:  " << v;
        break;
    }
}
void PythonConnection::ResponseFromPairing()
{
    qDebug() << "Pairing callback complete";
}
void PythonConnection::ConnectAgent()
{
    m_ifaceAgent = new QDBusInterface(AGENT_NAME,  // Service
                               "/org/law/pydbus/BruceAgent",           // Path
                               "org.law.pydbus.BruceAgent",    // Interface
                               QDBusConnection::sessionBus(),  // Bus
                               this);
   if (!m_ifaceAgent->isValid())
   {
      qDebug() << "Error connecting to python" << qPrintable(QDBusConnection::sessionBus().lastError().message());
      return;
   }
   qDebug() << "Connecting signal NotifyHost from agent";
   connect(m_ifaceAgent,SIGNAL(AgentToNotifyHost(int, QString)),this,SLOT(notificationFromAgent(int, QString)));
   qDebug() << "Agent connected";


}
void PythonConnection::notificationFromAgent(int v, QString message)
{
    qDebug() << "NOTIFICATION FROM PYTHON'S AGENT:  " << v;
    switch (v)
    {
    case AGENT_ERROR:
        m_pairedDeviceAddressString = "ERROR";
        qWarning() << "AN ERROR WAS SENT FROM PYTHON";
        break;
    case MESSAGE_ONE:
        qDebug() << "MESSAGE ONE FROM PYTHON IS:";
        qDebug() << message;
        ui->message->setText(message);
        this->show();
        break;
    case PAIR_COMPLETE:
        qDebug() << "MESSAGE TWO:";
        qDebug() << message;
        ui->message->setText(message);
        ui->justOkButtonBox->show();
        ui->buttonBox->hide();
        this->setWindowTitle("Device Paired");
        this->show();

        m_mainWindow->pairingSucceeded(message);
        break;
    default:
        qDebug() << ">>>>>> RECEIVED UNKNOWN CMD FROM PYTHON:  " << v;
        break;
    }
}

void PythonConnection::pairDevice(QString addressString)
{
    // start agent:
    m_iface->call("RunAgent");
    m_pairedDeviceAddressString = addressString;
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
int  PythonConnection::exec()
{
    qDebug() << "OK PRESSED";
    this->hide();

    return 0;
}
void PythonConnection::accept()
{
    qDebug() << "YES PRESSED";
    m_ifaceAgent->call("HostToAgentMessage", "YES");
    this->hide();

}
void PythonConnection::reject()
{
    qDebug() << "NO PRESSED";
    m_ifaceAgent->call("HostToAgentMessage", "NO");
    this->hide();
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
