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
    SELECT
        (1 - (SUM(CASE WHEN name = 'physical reads' THEN value ELSE 0 END) /
              (SUM(CASE WHEN name = 'consistent gets' THEN value ELSE 0 END) +
               SUM(CASE WHEN name = 'db block gets' THEN value ELSE 0 END)))) * 100 as Hit_Ratio
    FROM
        v$sysstat
    WHERE
        name IN ('physical reads', 'consistent gets', 'db block gets')
        ''')
        result = cursor.fetchone()[0]
        #print(result[0])
        #print(result)
        print("Hit ratio %.2f. | hitratio=%.2f" % (result, result))

        
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