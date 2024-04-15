import cx_Oracle
import sys

# Configuración de conexión
ORACLE_USER = sys.argv[1]
ORACLE_PASSWORD = sys.argv[2]
ORACLE_HOST = sys.argv[3]
ORACLE_PORT = '1521'
ORACLE_SID = sys.argv[4]

# Cadena de conexión completa
CONNECTION_STRING = f"{ORACLE_USER}/{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SID}"

def check_oracle_connection():
    cursor = ""
    connection = ""
        # Establecer conexión usando la cadena completa
    connection = cx_Oracle.connect(CONNECTION_STRING)

    # Ejecutar una consulta simple para verificar la conexión
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM DBA_DATAPUMP_JOBS
    ''')
    result = cursor.fetchall()
    print(result)
    try:

        # if int(result[0]) >= 1:
        #     print(f"CRITICAL - {result[0]} bloqueos. | bloqueos={result[0]}")
        #     sys.exit(2)
        # else:
        #     print(f"OK - No se encuentran bloqueos | bloqueos={result[0]}")
        #     sys.exit(0)
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