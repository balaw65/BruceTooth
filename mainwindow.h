#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "brucetoothpair.h"

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

private slots:
    void scanButtonPressed();
    void pairButtonPressed();
    void discoveredDeviceSelected();

private:
    Ui::MainWindow *ui;

    BruceToothPair m_bt;
    QString m_selectedDevicesAddress;

};

#endif // MAINWINDOW_H
