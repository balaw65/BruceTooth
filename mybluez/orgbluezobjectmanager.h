#ifndef ORGBLUEZOBJECTMANAGER_H
#define ORGBLUEZOBJECTMANAGER_H

#include <QtCore/QObject>
#include <QtCore/QByteArray>
#include <QtCore/QList>
#include <QtCore/QMap>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariant>
#include <QtDBus/QtDBus>

class OrgBluezObjectManager : public QDBusAbstractInterface
{
    Q_OBJECT
public:
    static inline const char *staticInterfaceName()
      { return "org.freedesktop.DBus.ObjectManager"; }

    OrgBluezObjectManager(const QString &service, const QString &path, const QDBusConnection &connection, QObject *parent = nullptr);
    ~OrgBluezObjectManager();

public Q_SLOTS:

    inline QDBusMessage GetManagedObjects()
    {
        return call(QStringLiteral("GetManagedObjects"));
    }

};

#endif // ORGBLUEZOBJECTMANAGER_H
