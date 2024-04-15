import pymssql
import sys

server = sys.argv[1]  
user = sys.argv[2] 
password = sys.argv[3] 


def mssql_connected_users():
    cursor = ""
    connection = ""
    try:
        connection = pymssql.connect(server, user, password)
        cursor = connection.cursor()   
        cursor.execute('''
                SELECT ((@@CPU_BUSY * CAST(@@TIMETICKS AS FLOAT)) /
                (SELECT (CAST(CPU_COUNT AS FLOAT) / CAST(HYPERTHREAD_RATIO AS FLOAT)) FROM sys.dm_os_sys_info) /
                100000000000)
                ''')
        result = cursor.fetchone()[0]
        if int(result) > 90:
            print(f"CRITICAL - CPU ocupada: {result} | cpu_used={result}")
            sys.exit(2)
        elif int(result) > 80:
            print(f"WARNING - CPU ocupada: {result} | cpu_used={result}")
            sys.exit(1)
        else:
            print(f"OK - CPU ocupada: {result} | cpu_used={result}")
            sys.exit(0)
    except Exception as e:
        print(f"CRITICAL - Error al conectarse a mssql: {e}")
        sys.exit(2)

if __name__ == "__main__":
    mssql_connected_users()