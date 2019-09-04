#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "brucetoothpair.h"
#include "pythonconnection.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();


    void addADiscoveredDevice(QString address, QString name, QBluetoothLocalDevice::Pairing pairingStatus);
    void addAScannedDevice(QString address, QString name);
    void scanComplete();
    void numberOfPairedDevices(int quantity);
    void pairingFailed();
    void pairingSucceeded();


    void unPairingFailed();
    void unPairingSucceeded();

private slots:
    void scanButtonPressed();
    void pairButtonPressed();
    void unpairButtonPressed();
    void discoveredDeviceSelected();
    void quitPython();
    void testButtonPressed();

private:
    Ui::MainWindow *ui;

    BruceToothPair m_bt;
    PythonConnection * m_pythonConnection;
    QString m_selectedDevicesAddress;
    QString m_pairedDeviceAddress;

};

#endif // MAINWINDOW_H
