#ifndef ORGBLUEZINTROSPECT_H
#define ORGBLUEZINTROSPECT_H

#include <QtCore/QObject>
#include <QtCore/QByteArray>
#include <QtCore/QList>
#include <QtCore/QMap>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariant>
#include <QtDBus/QtDBus>


class OrgBluezIntrospect : public QDBusAbstractInterface
{
    Q_OBJECT
public:
    static inline const char *staticInterfaceName()
    { return "org.freedesktop.DBus.Introspectable"; }

    OrgBluezIntrospect(const QString &service, const QString &path, const QDBusConnection &connection, QObject *parent = nullptr);
    ~OrgBluezIntrospect();

public Q_SLOTS:
    inline QDBusReply<QString> Introspect()
    {
        qDebug() << "Inline Introspect called";
        return asyncCall(QStringLiteral("Introspect"));
    }

};

#endif // ORGBLUEZINTROSPECT_H
