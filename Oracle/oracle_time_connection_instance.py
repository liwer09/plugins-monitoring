import cx_Oracle
import sys
import datetime

# Configuración de conexión
ORACLE_USER = sys.argv[1]
ORACLE_PASSWORD = sys.argv[2]
ORACLE_HOST = sys.argv[3]
ORACLE_PORT = '1521'
ORACLE_SID = sys.argv[4]
ORACLE_INSTANCE = sys.argv[5]

# Cadena de conexión completa

CONNECTION_STRING = f"{ORACLE_USER}/{ORACLE_PASSWORD}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={ORACLE_HOST})(PORT={ORACLE_PORT}))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME={ORACLE_SID})(INSTANCE_NAME={ORACLE_INSTANCE})))"
def check_oracle_connection():
    try:
        # Obtenemos la hora antes de establecer conexión usando la cadena completa
        t1 = datetime.datetime.now()
        connection = cx_Oracle.connect(CONNECTION_STRING)
        # Volvemos a obtener la hora tras haber realizado la conexion.
        t2 = datetime.datetime.now()
        #restamos los tiempos para obtener los segundos de conexion.
        totaltime = t2 - t1
        if totaltime.total_seconds() >= 5:
            print("CRITICAL - %.2f seconds to connect as %s. | time=%.2f" % (float(totaltime.total_seconds()),str(ORACLE_SID),float(totaltime.total_seconds())))
            sys.exit(2)
        elif totaltime.total_seconds() >= 3:
            print("WARNING - %.2f seconds to connect as %s. | time=%.2f" % (float(totaltime.total_seconds()),str(ORACLE_SID),float(totaltime.total_seconds())))
            sys.exit(1)
        else:
            print("OK - %.2f seconds to connect as %s. | time=%.2f" % (float(totaltime.total_seconds()),str(ORACLE_SID),float(totaltime.total_seconds())))
            sys.exit(0)

    #Si falla al conectarse, reportamos el error.
    except cx_Oracle.DatabaseError as e:
        print(f"CRITICAL - Error al conectarse a Oracle: {e}")
        sys.exit(2)

if __name__ == "__main__":
    check_oracle_connection()