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
    try:
        # Establecer conexión usando la cadena completa
        connection = cx_Oracle.connect(CONNECTION_STRING)
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor = connection.cursor()
        cursor.execute('''
            select owner, job_name,last_start_date, failure_count from dba_scheduler_jobs where enabled='TRUE' and STATE IN ('BROKEN','FAILED') and owner = 'GICNETCAJA'
        ''')
        result = cursor.fetchall()
        #print(result[0])
        if len(result) == 0:
            print("No hay fallos en la ejecucion de Jobs")
        else:
            errores = ""
            for i in result:
                errores = errores + i + ", "
            print(f"Errores en la ejecucion de logs: {errores}")
            sys.exit(1)
        
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