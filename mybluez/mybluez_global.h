#ifndef MYBLUEZ_GLOBAL_H
#define MYBLUEZ_GLOBAL_H

#include <QtCore/qglobal.h>

#if defined(MYBLUEZ_LIBRARY)
#  define MYBLUEZSHARED_EXPORT Q_DECL_EXPORT
#else
#  define MYBLUEZSHARED_EXPORT Q_DECL_IMPORT
#endif

#endif // MYBLUEZ_GLOBAL_H
