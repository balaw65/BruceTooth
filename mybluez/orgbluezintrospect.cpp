#include "orgbluezintrospect.h"

OrgBluezIntrospect::OrgBluezIntrospect(const QString &service, const QString &path, const QDBusConnection &connection, QObject *parent)
    : QDBusAbstractInterface(service, path, staticInterfaceName(), connection, parent)
{

}
OrgBluezIntrospect::~OrgBluezIntrospect()
{
}
