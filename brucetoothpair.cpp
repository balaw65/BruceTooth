#include "brucetoothpair.h"
#include "mainwindow.h"
#include <QDebug>
#include <QBluetoothLocalDevice>


BruceToothPair::BruceToothPair(QObject *parent) : QObject(parent)
{
   m_mainWindow = nullptr;
   m_pairDevice = false;
   m_this = this;
   m_pairFailCount = 0;
   m_btNumberOfPairedDevices = 0;

}
int BruceToothPair::list()
{
   return 0;
}
QString BruceToothPair::getAddressOfLocalDevice()
{
    return ""; //m_localDevice->address().toString();
}
void BruceToothPair::powerOn()
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
//   m_localDevice->powerOn();
}
void BruceToothPair::powerOff()
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
//   m_localDevice->setHostMode(QBluetoothLocalDevice::HostPoweredOff);
}
void BruceToothPair::setAgent()
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
//   m_localDevice->setHostMode(QBluetoothLocalDevice::HostDiscoverable);
}
void BruceToothPair::setDefaultAgent()
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
    //discoveryAgent->setInquiryType()
}
void BruceToothPair::scanOn()
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
   m_discoveryAgent = new QBluetoothDeviceDiscoveryAgent();
   powerOff();
   powerOn();
   setAgent();
   setDefaultAgent();

   m_discoveryAgent->start();
   connect(m_discoveryAgent, SIGNAL(deviceDiscovered(QBluetoothDeviceInfo)),this, SLOT(deviceFound(QBluetoothDeviceInfo)));
   connect(m_discoveryAgent, SIGNAL(finished()), this, SLOT(scanFinished()));

}
void BruceToothPair::deviceFound(QBluetoothDeviceInfo info)
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
   qDebug() << "Device Found:  " << info.address();
   if (m_mainWindow != nullptr)
   {
       m_mainWindow->addAScannedDevice(info.address().toString(), info.name());
   }
}
void BruceToothPair::scanFinished()
{
    qDebug() << __FILE__ << ":" << __FUNCTION__;
   qDebug() << "DONE SCANNING";
   int Devices = 0;
   m_mainWindow->scanComplete();
   m_found_devices =  m_discoveryAgent->discoveredDevices();
   foreach (QBluetoothDeviceInfo info, m_found_devices)
   {
      m_mainWindow->addADiscoveredDevice(info.address().toString(), info.name(),
                                          m_localDevice->pairingStatus(info.address()));

      switch (m_localDevice->pairingStatus(info.address()))
      {
         case QBluetoothLocalDevice::Unpaired:
              break;
         case QBluetoothLocalDevice::Paired:
              m_btPairedDevicesAddress = info.address();
              m_btNumberOfPairedDevices++;

              break;
         case QBluetoothLocalDevice::AuthorizedPaired:
              m_btPairedDevicesAddress = info.address();
              m_btNumberOfPairedDevices++;
              break;
      }
   }
   if ( m_btNumberOfPairedDevices == 0)
       m_btPairedDevicesAddress.clear();
   m_mainWindow->numberOfPairedDevices(m_btNumberOfPairedDevices);
}
#if 0
void BruceToothPair::displayPin(const QBluetoothAddress &address, QString pin)
{
   qDebug() << "Pin display for " << address.toString() << " is " << pin;
}
void BruceToothPair::displayConfirmation(const QBluetoothAddress &address, QString pin)
{
   qDebug() << "Pin confirmation for " << address.toString() << " is " << pin;
}
void BruceToothPair::displayConfAccepted()
{
    qDebug() << "Display Confirmation Accpet";
}
void BruceToothPair::displayConfReject()
{
    qDebug() << "Display Confirmation Reject";
}
void BruceToothPair::serviceDiscovered(const QBluetoothServiceInfo &serviceInfo)
{
    qDebug() << "Service Info: ";
    qDebug() << "   name:  " << serviceInfo.serviceName();
}
void BruceToothPair::serviceDiscoveryFinished()
{
   qDebug() << "Display Confirmation Reject";
}

void BruceToothPair::dbusError()
{
   qDebug() << "\n\n\nDBUS ERROR....\n\n\n";
}


void BruceToothPair::pairDevice(QString atAddress)
{
   QDBusInterface manager("org.bluez", "/",  "org.freedesktop.DBus.ObjectManager", QDBusConnection::systemBus());
   QDBusReply<void> reply = manager.call("GetManagedObjects");






   /* First, find paired devices: */
   m_btPairedDevicesAddress = QBluetoothAddress(atAddress);

   /* Display pin: */
   connect(m_localDevice, SIGNAL(pairingDisplayPinCode(QBluetoothAddress, QString)), this, SLOT(displayPin(QBluetoothAddress, QString)));
   /* Confirm pin: */
   connect(m_localDevice, SIGNAL(pairingDisplayConfirmation(QBluetoothAddress, QString)), this, SLOT(displayConfirmation(QBluetoothAddress, QString)));

   m_localDevice->requestPairing(m_btPairedDevicesAddress, QBluetoothLocalDevice::Paired);


}
void BruceToothPair::pairingDone(const QBluetoothAddress &address, QBluetoothLocalDevice::Pairing pair)
{
   qDebug() << "Pairing Done for:  " << address.toString();
}
void BruceToothPair::pairingFailure(QBluetoothLocalDevice::Error error)
{
   qDebug() << "Pairing Failed, reason:  ";
   switch (error)
   {
     case QBluetoothLocalDevice::PairingError:
       qDebug() << "Pairing Error...";
       m_pairFailCount++;
       if (m_pairFailCount < 2)
       {
           qDebug() << "Trying again, this time using Authorized Pairing for: " << m_btPairedDevicesAddress.toString();
           m_localDevice->requestPairing(m_btPairedDevicesAddress, QBluetoothLocalDevice::AuthorizedPaired);
       }
       else
       {
           qDebug() << "Arg, giving up";
       }
       break;
     case QBluetoothLocalDevice::UnknownError:
     default:
       qDebug() << "Unknown Error...";
       break;


   }

   m_mainWindow->pairingFailed();

}
bool BruceToothPair::waitForService(const QString &serviceName, const QDBusConnection &bus)
{
    if (bus.interface()->registeredServiceNames().value().contains(serviceName))
    {
        return true;
    }

    qDebug() << "Service not ready yet";


    return false;
}
#endif
void BruceToothPair::setMainWindow(MainWindow *mw)
{
    m_mainWindow = mw;
}
