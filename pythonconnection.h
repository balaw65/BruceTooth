#ifndef PYTHONCONNECTION_H
#define PYTHONCONNECTION_H

#include <QObject>

class PythonConnection : public QDBusAbstractAdapter
{
public:
    PythonConnection();
};

#endif // PYTHONCONNECTION_H
