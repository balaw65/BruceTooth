#ifndef PYTHONCONNECTION_H
#define PYTHONCONNECTION_H

#include "ui_pymessage.h"

#include <QtCore/QObject>
#include <QtCore/QFile>
#include <QtDBus/QDBusVariant>
#include <QtDBus/QDBusInterface>

#include <QDialog>

#define SERVICE_NAME "org.law.pydbus.BruceTooth"
#define AGENT_NAME   "org.law.pydbus.BruceAgent"

enum {
    NOTIFICATION_ERROR = -1,
    PAIRED_SUCCESS     =  1,
    PASSKEY_MESSAGE    =  2,
    CONNECT_AGENT      =  5
     };
enum {
    AGENT_ERROR        = -1,
    MESSAGE_ONE        = 1,
    PAIR_COMPLETE      = 2,

};

class MainWindow;
class PythonConnection:public QDialog
{
    Q_OBJECT

public:
    PythonConnection(QWidget * parent = nullptr);
    ~PythonConnection();

    int connectInterface();
    QString getPairedDevices();
    void pairDevice(QString addressString);
    void startAgent();
    void killAgent();
    void quitPython();
    void test();

    void setMainWindow(MainWindow * value);
    MainWindow * getMainWindow();

public slots:
    void notification(int, QString);
    void notificationFromAgent(int, QString);
    void ResponseFromPairing();

    void accept() override;
    void reject() override;
    int  exec()   override;


private:

    void ConnectAgent();
    QDBusInterface * m_iface;
    QDBusInterface * m_ifaceAgent;



    QString        m_pairedDeviceAddressString;
    MainWindow     * m_mainWindow;

    Ui_PyMessage   * ui;





#if 0
signals:
    void messageFromPython();
public slots:
    void sendMessageToPython(const QString &query);
#endif
};

#endif // PYTHONCONNECTION_H
