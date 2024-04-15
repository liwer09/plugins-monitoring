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
    status = 0
    connection = ""
    try:
        # Establecer conexión usando la cadena completa
        connection = cx_Oracle.connect(CONNECTION_STRING)
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor = connection.cursor()
        cursor.execute('''
            Select count(*) n from (select idtransaccion from gicnetcaja.replicasync group by idtransaccion)
        ''')
        result = cursor.fetchone()
        if result[0] > 5000:
            print(f"CRITICAL: Numero de transacciones: {result[0]} | transacciones={result[0]}")
            status = 2
        elif result[0] > 500:
            print(f"WARNING: Numero de transacciones: {result[0]} | transacciones={result[0]}")
            status = 1
        else:
            print(f"OK: Numero de transacciones: {result[0]} | transacciones={result[0]}")
            status = 0

        
    except cx_Oracle.DatabaseError as e:
        print(f"CRITICAL - Error al conectarse a Oracle: {e}")
        sys.exit(2)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        sys.exit(int(status))

if __name__ == "__main__":
    check_oracle_connection()