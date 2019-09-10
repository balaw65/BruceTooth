#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    bool usePython = true;

    m_pythonConnection = new PythonConnection(this);
    if (m_pythonConnection->connectInterface() != 0)
    {
        qDebug() << "Error connecting to python bus";
        usePython = false;
    }

    m_bt.setMainWindow(this);

    ui->foundDevicesListWidget->setEnabled(false);
    ui->discoveredDevicesListWidget->setEnabled(false);
    ui->pairButton->setEnabled(false);
    ui->unPairButton->setEnabled(false);
    if (usePython)
    {
       m_pairedDeviceAddress = m_pythonConnection->getPairedDevices();
       ui->pairedDeviceAddress->setText(m_pairedDeviceAddress);
       if (m_pairedDeviceAddress.split(":").count() == 6)
         ui->unPairButton->setEnabled(true);
    }
    else
    {
       //m_pythonConnection->getPairedDevices()
       m_pairedDeviceAddress = "UNKNOWN";
       ui->pairedDeviceAddress->setText("UNKNOWN");
    }

    /* List local devices: */
    int numberOfLocalDevices = m_bt.list();
    if (numberOfLocalDevices == 0)
    {
        ui->localDeviceAddress->setText("NONE FOUND");
        ui->scanButton->setEnabled(false);
    }
    else if (numberOfLocalDevices > 1)
    {
        ui->localDeviceAddress->setText("MULTIPLE DEVICES FOUND");
        ui->scanButton->setEnabled(false);

    }
    else
    {
        ui->localDeviceAddress->setText(m_bt.getAddressOfLocalDevice());
        ui->scanButton->setEnabled(true);
    }

    connect(ui->scanButton,   SIGNAL(clicked()), this, SLOT(scanButtonPressed()));
    connect(ui->pairButton,   SIGNAL(clicked()), this, SLOT(pairButtonPressed()));
    connect(ui->unPairButton, SIGNAL(clicked()), this, SLOT(unpairButtonPressed()));

    connect(ui->discoveredDevicesListWidget, SIGNAL(itemSelectionChanged()), this, SLOT(discoveredDeviceSelected()));

    connect(ui->quitPythonButton, SIGNAL(clicked()), this, SLOT(quitPython()));
    connect(ui->testPushButton,   SIGNAL(clicked()), this, SLOT(testButtonPressed()));
}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::scanButtonPressed()
{
   qDebug() << "SCAN BUTTON PRESSED";
   ui->foundDevicesListWidget->setEnabled(true);
   ui->discoveredDevicesListWidget->clear();
   ui->discoveredDevicesListWidget->setEnabled(false);
   ui->scanButton->setEnabled(false);
   this->setCursor(Qt::WaitCursor);

   m_bt.scanOn();
}
void MainWindow::pairButtonPressed()
{
    qDebug() << "Pair Button Pressed, attempting to pair device at address |" << m_selectedDevicesAddress << "|";
    ui->pairButton->setEnabled(false);
    ui->foundDevicesListWidget->setEnabled(false);
    m_pythonConnection->pairDevice(m_selectedDevicesAddress);
    //this->setCursor(Qt::WaitCursor);
}
void MainWindow::unpairButtonPressed()
{
     qDebug() << "UnPair Button Pressed, attempting to unpair device at address |" <<
                 m_pairedDeviceAddress << "|";
     m_bt.unPairDevice(m_pairedDeviceAddress);
}
void MainWindow::pairingFailed()
{
    ui->pairedDeviceAddress->setText("PAIRING FAILED");
    this->setCursor(Qt::ArrowCursor);
    ui->pairButton->setEnabled(true);

}
void MainWindow::pairingSucceeded()
{

}
void MainWindow::unPairingFailed()
{
    qDebug() << "Un-pairing attempt failed";
    ui->pairedDeviceAddress->setText("PAIRING FAILED");
    this->setCursor(Qt::ArrowCursor);
    ui->pairButton->setEnabled(true);

}
void MainWindow::unPairingSucceeded()
{
    qDebug() << "Un-pairing attempt successful";
    ui->pairButton->setEnabled(true);
    ui->unPairButton->setEnabled(false);
    m_pairedDeviceAddress = "";
    ui->pairedDeviceAddress->setText("NOTHING PAIRED");

}

void MainWindow::addADiscoveredDevice(QString address, QString name, QBluetoothLocalDevice::Pairing paired)
{
   QString item = "";
   item.append(address);
   item.append("   |   ");
   item.append(name);
   ui->discoveredDevicesListWidget->addItem(item);
   switch (paired)
   {
     case QBluetoothLocalDevice::Unpaired:
          break;
     case QBluetoothLocalDevice::Paired:
     case QBluetoothLocalDevice::AuthorizedPaired:
          ui->pairedDeviceAddress->setText(address);
          break;
   }
}

void MainWindow::numberOfPairedDevices(int quantity)
{
    if ( quantity == 0 )
    {
        ui->unPairButton->setEnabled(false);
        ui->pairedDeviceAddress->setText("NONE");
    }
    else if (quantity == 1)
    {
        ui->unPairButton->setEnabled(true);
        //ui->pairedDeviceAddress->setText(m_bt.getAddressOfPairedDevice());
    }
    else
    {
        ui->unPairButton->setEnabled(false);
        ui->pairedDeviceAddress->setText("> 1 device is paired???");
    }

}
void MainWindow::scanComplete()
{
    ui->foundDevicesListWidget->setEnabled(false);
    ui->discoveredDevicesListWidget->setEnabled(true);
    ui->scanButton->setEnabled(true);
    this->setCursor(Qt::ArrowCursor);
}
void MainWindow::addAScannedDevice(QString address, QString name)
{
    QString item = "";
    item.append(address);
    item.append("   |   ");
    item.append(name);
    ui->foundDevicesListWidget->addItem(item);
}
void MainWindow::discoveredDeviceSelected()
{
    qDebug() << "DISCOVERED DEVICE SELECTED...";
    QList<QListWidgetItem *> items =   ui->discoveredDevicesListWidget->selectedItems();
    m_selectedDevicesAddress = "";
    if (items.count() == 1)
    {
       m_selectedDevicesAddress = items.first()->text().split('|').first().trimmed();
       ui->pairButton->setEnabled(true);

       qDebug() << "Address of selected item:  " << m_selectedDevicesAddress;
    }
    else {
        ui->pairButton->setEnabled(false);
    }
}
void MainWindow::quitPython()
{
   qDebug() << "QUIT PYTHON BUTTON PRESSED";
   m_pythonConnection->quitPython();
}
void MainWindow::testButtonPressed()
{
   qDebug() << "TEST BUTTON PRESSED";
   //m_pythonConnection->pairDevice("CC:44:63:20:D0:5F");
   m_pythonConnection->test();
}
