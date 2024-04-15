import cx_Oracle
import sys

# Configuración de conexión
ORACLE_USER = sys.argv[1]
ORACLE_PASSWORD = sys.argv[2]
ORACLE_HOST = sys.argv[3]
ORACLE_PORT = '1521'
ORACLE_SID = sys.argv[4]
WARNING = sys.argv[5]
CRITICAL = sys.argv[6]

# Cadena de conexión completa
CONNECTION_STRING = f"{ORACLE_USER}/{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SID}"

def check_oracle_connection():
    try:
        # Establecer conexión usando la cadena completa
        connection = cx_Oracle.connect(CONNECTION_STRING)
        exit = 0
        # Ejecutar una consulta simple para verificar la conexión
        cursor = connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM gv$session WHERE type = 'USER' AND username = 'GICNET' ''')
        result = cursor.fetchall()
        if len(result) >= int(CRITICAL):
            exit = 2
        elif len(result) >= int(WARNING):
            exit = 1
        print("%i conexiones simultaneas. | conexiones=%i" % (len(result),len(result)))
        sys.exit(exit)

        
    except cx_Oracle.DatabaseError as e:
        print(f"CRITICAL - Error al conectarse a Oracle: {e}")
        sys.exit(2)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    check_oracle_connection()