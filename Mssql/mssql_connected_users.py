import pymssql
import sys

server = sys.argv[1]  
user = sys.argv[2] 
password = sys.argv[3]
port = "1766"


def mssql_connected_users():
    cursor = ""
    connection = ""
    try:
        connection = pymssql.connect(server, user, password)
        cursor = connection.cursor()   
        cursor.execute("SELECT COUNT(*) as user_count FROM sys.dm_exec_sessions WHERE is_user_process = 1")
        result = cursor.fetchone()[0]
        if int(result) > 20:
            print(f"CRITICAL - Numero de conexiones: {result} | conexiones={result}")
            sys.exit(2)
        elif int(result) > 10:
            print(f"WARNING - Numero de conexiones: {result} | conexiones={result}")
            sys.exit(1)
        else:
            print(f"OK - Numero de conexiones: {result} | conexiones={result}")
            sys.exit(0)
    except Exception as e:
        print(f"CRITICAL - Error al conectarse a mssql: {e}")
        sys.exit(2)

if __name__ == "__main__":
    mssql_connected_users()