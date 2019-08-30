#ifndef MYBLUEZ_H
#define MYBLUEZ_H

#include "mybluez_global.h"

#include "orglocaldevicechangeinterface.h"
#include "orgbluezintrospect.h"
#include "orgbluezobjectmanager.h"

#include <QMap>
#include <QString>
#include <QList>


class MYBLUEZSHARED_EXPORT Mybluez : public QObject
{

    Q_OBJECT

public:
    explicit Mybluez(QObject *parent = nullptr);
    virtual ~Mybluez();


    void getDevices();
    void getIntrospectable();
    void getManagedObjects();


public slots:
    QObject * resultsFromGetDevices(QDBusMessage message);
    QObject * resultsFromGetDevices(QDBusReply<QList<QVariantMap>> reply);

    QObject * resultsFromGetIntrospect(QDBusMessage message);
    QObject * resultsFromGetIntrospect(QDBusReply<QString> reply);

    const char * errorFromGetDevices();



    void changed();
    void deviceAdded(QMap<QString,QVariant> v0);
    void deviceChanged(QMap<QString,QVariant> v0);
    void deviceRemoved(QMap<QString,QVariant> v0);
private:
    OrgLocalDeviceChangeInterface * m_aDevice;
    OrgBluezIntrospect            * m_anIntrospection;
    OrgBluezObjectManager         * m_managedObject;

};

#endif // MYBLUEZ_H
