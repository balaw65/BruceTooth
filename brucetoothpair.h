#ifndef BRUCETOOTHPAIR_H
#define BRUCETOOTHPAIR_H

#include <QObject>
#include <QTimer>
#include <QBluetoothDeviceDiscoveryAgent>
#include <QBluetoothLocalDevice>

class MainWindow;

class BruceToothPair : public QObject
{
    Q_OBJECT
public:
    explicit BruceToothPair(QObject *parent = nullptr);

    QString getAddressOfLocalDevice(); //Ok
    int  list(); // Ok
    void pairDevice(QString atAddress);
    void unPairDevice(QString atAddress);

    void scanOn(); // Ok
    void setMainWindow(MainWindow * mw); // Ok

    void powerOn(); // Ok
    void powerOff(); // Ok

public slots:
    void scanFinished(); // Ok
    void pairingUnpairingDone(
              const QBluetoothAddress&,
              QBluetoothLocalDevice::Pairing);



private slots:


    void serviceDiscoveryFinished(); // Ok
    void deviceFound(QBluetoothDeviceInfo info); //OK


private:

    void setAgent(); // Ok
    void setDefaultAgent(); // Ok



    bool m_pairDevice;
    QTimer * pairingStatusTimer;
    int m_pairFailCount;
    int m_btNumberOfPairedDevices;
    QBluetoothAddress m_btPairedDevicesAddress;


    MainWindow * m_mainWindow;
    BruceToothPair * m_this;


    QBluetoothDeviceDiscoveryAgent * m_discoveryAgent;
    QBluetoothLocalDevice * m_localDevice;
    QList<QBluetoothDeviceInfo> m_found_devices;


};

#endif // BRUCETOOTHPAIR_H
