#ifndef PYTHONCONNECTION_H
#define PYTHONCONNECTION_H

#include <QtCore/QObject>
#include <QtCore/QFile>
#include <QtDBus/QDBusVariant>
#include <QtDBus/QDBusInterface>

#define SERVICE_NAME "org.law.pydbus.BruceTooth"
class MainWindow;
class PythonConnection:public QObject
{
    Q_OBJECT

public:
    PythonConnection(QObject * obj);
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
    void notification(int);


private:
    QDBusInterface * m_iface;
    QString        m_pairedDeviceAddressString;
    MainWindow     * m_mainWindow;



#if 0
signals:
    void messageFromPython();
public slots:
    void sendMessageToPython(const QString &query);
#endif
};

#endif // PYTHONCONNECTION_H
