import cx_Oracle
import sys

# Configuración de conexión
ORACLE_USER = sys.argv[1]
ORACLE_PASSWORD = sys.argv[2]
ORACLE_HOST = sys.argv[3]
ORACLE_PORT = '1521'
ORACLE_SID = sys.argv[4]
ORACLE_DISKGROUP = sys.argv[5]

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
        cursor.execute(f'''
            SELECT
                name AS disk_group_name,
                total_mb AS total_size_mb,
                free_mb AS free_size_mb,
                ROUND((total_mb - free_mb) / total_mb * 100, 2) AS used_percentage
            FROM
                V$ASM_DISKGROUP
            WHERE
                name = '{ORACLE_DISKGROUP}'
        ''')
        result = cursor.fetchone()
        if float(result[3]) >= 90:
            print(f"CRITICAL - {ORACLE_DISKGROUP} Diskgroup used space: {result[3]}%")
            sys.exit(2)
        elif float(result[3]) >= 80:
            print(f"WARNING - {ORACLE_DISKGROUP} Diskgroup used space: {result[3]}%")
            sys.exit(1)
        else:
            print(f"OK - {ORACLE_DISKGROUP} Diskgroup used space: {result[3]}%")
            sys.exit(0)

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