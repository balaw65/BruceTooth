#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    m_bt.setMainWindow(this);

    ui->foundDevicesListWidget->setEnabled(false);
    ui->discoveredDevicesListWidget->setEnabled(false);
    ui->pairButton->setEnabled(false);
    ui->unPairButton->setEnabled(false);
    ui->pairedDeviceAddress->setText("UNKOWN");

    /* List local devices: */
    if ( m_bt.list() != 0)
    {
        ui->localDeviceAddress->setText("NONE FOUND");
        ui->scanButton->setEnabled(false);
    }
    else
    {
        ui->localDeviceAddress->setText(m_bt.getAddressOfLocalDevice());
        ui->scanButton->setEnabled(true);
    }

    connect(ui->scanButton, SIGNAL(clicked()), this, SLOT(scanButtonPressed()));
    connect(ui->pairButton, SIGNAL(clicked()), this, SLOT(pairButtonPressed()));

    connect(ui->discoveredDevicesListWidget, SIGNAL(itemSelectionChanged()), this, SLOT(discoveredDeviceSelected()));
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
    this->setCursor(Qt::WaitCursor);
    //m_bt.pairDevice(m_selectedDevicesAddress);
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

