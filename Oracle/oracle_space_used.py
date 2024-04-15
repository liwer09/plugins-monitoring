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
    try:
        # Establecer conexión usando la cadena completa
        connection = cx_Oracle.connect(CONNECTION_STRING)
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor = connection.cursor()
        cursor.execute('''
            select round(sum(bytes)/(1024*1024*1024),2) ocupacio
            from sys.dba_extents a, sys.dba_tablespaces b
            where a.tablespace_name = b.tablespace_name
            and a.tablespace_name not in ('SYSTEM','UNDO','TEMP','SYSAUX')
        ''')
        result = cursor.fetchone()
        #print(result[0])
        print("OK - El consumo de disco es de %.2f GB. | espacio_usado=%.2f" %(float(result[0]), float(result[0])))

        
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