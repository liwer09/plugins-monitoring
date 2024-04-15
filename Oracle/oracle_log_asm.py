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
             Select space_used/1024/1024 as mb_space, round(space_used*100/space_limit, 0) as pct_space,  number_of_files from v$recovery_file_dest
        ''')
        result = cursor.fetchall()[0]
        if result[1] > 80:
            print(f"CRITICAL: Espacio utilizado: {result[0]} MB - Espacio utilizado en %: {result[1]}% - Numero de archivos: {result[2]} | mb_space={result[0]} | pct_space={result[1]} | number_files={result[2]}")
            sys.exit(2)
        elif result[1] > 60:
            print(f"WARNING: Espacio utilizado: {result[0]} MB - Espacio utilizado en %: {result[1]}% - Numero de archivos: {result[2]} | mb_space={result[0]} | pct_space={result[1]} | number_files={result[2]}")
            sys.exti(1)
        else:
            print(f"OK: Espacio utilizado: {result[0]} MB - Espacio utilizado en %: {result[1]}% - Numero de archivos: {result[2]} | mb_space={result[0]} | pct_space={result[1]} | number_files={result[2]}")
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