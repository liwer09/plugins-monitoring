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
    metrics = ""
    exit_code = 0
    try:
        # Establecer conexión usando la cadena completa
        connection = cx_Oracle.connect(CONNECTION_STRING)
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor = connection.cursor()
        cursor.execute('''
            SELECT name, (1 - (free_mb / total_mb)) * 100 AS porcentaje_de_uso FROM v$asm_diskgroup
        ''')
        result = cursor.fetchall()
        for i in result:
            if i[1] >= 100:
                exit_code = 2
            elif i[1] > 95:
                exit_code = 1
            metrics = f"{metrics} {str(i[0])}={round(i[1], 2)}"
        print(f" Diskgroup used space:{metrics} | {metrics}")
        sys.exit(exit_code)
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