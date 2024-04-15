import pymssql
import sys
import datetime

server = sys.argv[1]  
user = sys.argv[2] 
password = sys.argv[3] 


def mssql_connected_users():
    cursor = ""
    connection = ""
    try:
        t1 = datetime.datetime.now()
        connection = pymssql.connect(server, user, password)
        t2 = datetime.datetime.now()
        totaltime = t2 - t1
        print(f"OK - Tiempo de conexion: {round(totaltime.total_seconds(), 2)} s. | tiempo={round(totaltime.total_seconds(), 2)}")
        connection.close()
        sys.exit(0)
    except Exception as e:
        print(f"CRITICAL - Error al conectarse a mssql: {e}")
        sys.exit(2)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        

if __name__ == "__main__":
    mssql_connected_users()