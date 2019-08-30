#ifndef ORGLOCALDEVICECHANGEINTERFACE_H
#define ORGLOCALDEVICECHANGEINTERFACE_H

#include <QtCore/QObject>
#include <QtCore/QByteArray>
#include <QtCore/QList>
#include <QtCore/QMap>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariant>
#include <QtDBus/QtDBus>

#include <QObject>
#include <QMap>
#include <QString>

class OrgLocalDeviceChangeInterface : public QDBusAbstractInterface
{
    Q_OBJECT
public:
    static inline const char *staticInterfaceName()
    { return "org.freedesktop.fwupd"; }

    QObject * resultsFromGetDevices(){return nullptr;}
    const char * errorFromGetDevices(){return nullptr;}
public:
    OrgLocalDeviceChangeInterface(const QString &service, const QString &path, const QDBusConnection &connection, QObject *parent = nullptr);
    ~OrgLocalDeviceChangeInterface();


public Q_SLOTS:

    inline QDBusMessage GetDevices()
    {
        return call(QDBus::Block, QStringLiteral("GetDevices"));
    }
    inline QDBusReply<QVariantMap> GetHistory()
    {
        QList<QVariant> argumentList;
        return asyncCallWithArgumentList(QStringLiteral("GetHistory"), argumentList);
    }


Q_SIGNALS:
    void Changed();
    void DeviceAdded(const QMap<QString,QVariant> in0);
    void DeviceChanged(const QMap<QString,QVariant> in0);
    void DeviceRemoved(const QMap<QString,QVariant> in0);

};

#endif // ORGLOCALDEVICECHANGEINTERFACE_H
