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

    int  list();

    void scanOn();
    void pairDevice(QString atAddress);

    QString getAddressOfLocalDevice();

    void setMainWindow(MainWindow * mw);


public slots:
    void scanFinished();
private slots:

    void displayConfAccepted();
    void displayConfReject();

    void serviceDiscoveryFinished();
    void deviceFound(QBluetoothDeviceInfo info);


private:

    void powerOn();
    void powerOff();
    void setAgent();
    void setDefaultAgent();



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
