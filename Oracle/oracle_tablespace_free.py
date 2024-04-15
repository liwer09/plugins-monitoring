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
        
        # Ejecutamos la query para obtener los datos de espacio usado con autoexpand de las BBDD de Oracle.
        cursor = connection.cursor()
        cursor.execute('''
            WITH tbs_auto AS (
                SELECT DISTINCT tablespace_name, autoextensible
                FROM dba_data_files
                WHERE autoextensible = 'YES' AND tablespace_name NOT LIKE 'UNDO%'
            ),
            files AS (
                SELECT tablespace_name, COUNT(*) tbs_files, SUM(BYTES) total_tbs_bytes
                FROM dba_data_files
                WHERE tablespace_name NOT LIKE 'UNDO%'
                GROUP BY tablespace_name
            ),
            fragments AS (
                SELECT tablespace_name, COUNT(*) tbs_fragments, SUM(BYTES) total_tbs_free_bytes, MAX(BYTES) max_free_chunk_bytes
                FROM dba_free_space
                WHERE tablespace_name NOT LIKE 'UNDO%'
                GROUP BY tablespace_name
            ),
            AUTOEXTEND AS (
                SELECT tablespace_name, SUM(size_to_grow) total_growth_tbs
                FROM (
                    SELECT file_name, tablespace_name, MAX(size_to_grow) size_to_grow
                    FROM (
                        SELECT file_name, tablespace_name, maxbytes size_to_grow
                        FROM dba_data_files
                        WHERE tablespace_name NOT LIKE 'UNDO%'
                        UNION ALL
                        SELECT file_name, tablespace_name, BYTES size_to_grow
                        FROM dba_data_files
                        WHERE tablespace_name NOT LIKE 'UNDO%'
                    )
                    GROUP BY file_name, tablespace_name
                )
                GROUP BY tablespace_name
            )
            SELECT a.tablespace_name,
                CASE tbs_auto.autoextensible
                    WHEN 'YES' THEN 'YES'
                    ELSE 'NO'
                END AS autoextensible,
                files.tbs_files files_in_tablespace,
                files.total_tbs_bytes / 1024 / 1024 total_tablespace_space,
                COALESCE((files.total_tbs_bytes - fragments.total_tbs_free_bytes) / 1024 / 1024, files.total_tbs_bytes / 1024 / 1024) total_used_space,
                COALESCE(fragments.total_tbs_free_bytes / 1024 / 1024, 0) total_tablespace_free_space,
                COALESCE((((files.total_tbs_bytes - fragments.total_tbs_free_bytes) / files.total_tbs_bytes) * 100), 100) total_used_pct,
                AUTOEXTEND.total_growth_tbs / 1024 / 1024 max_size_of_tablespace,
                COALESCE((((files.total_tbs_bytes - fragments.total_tbs_free_bytes) / AUTOEXTEND.total_growth_tbs) * 100), 100) total_auto_used_pct
            FROM dba_tablespaces a, files, fragments, AUTOEXTEND, tbs_auto
            WHERE a.tablespace_name = files.tablespace_name
            AND a.tablespace_name = fragments.tablespace_name(+)
            AND a.tablespace_name = AUTOEXTEND.tablespace_name
            AND a.tablespace_name = tbs_auto.tablespace_name(+)
            ORDER BY total_auto_used_pct DESC
        ''')
        exit = 0
        metrics = ""
        result = cursor.fetchall()
        #Recorremos el resultado de la query, generamos una variable para obtener el espacio libre restandole a 100 el utlimo valor de la query.
        for i in result:
            espacio_disponible = 100 - float(i[-1])
            #formateamos el string a mostrar
            metrics = metrics + " %s=%.2f" % (str(i[0]),float(espacio_disponible))
            #Revisamos que ningun diskspace sea inferior a 2% o 5%.
            if exit != 2:
                if espacio_disponible < 2.00:
                    exit = 2
                elif espacio_disponible < 5.00:
                    exit = 1
                else:
                    continue
        #Hacemos un print del texto y pasamos el codigo de cierre.
        print("Espacio libre en las tablespaces %s |%s" % (str(metrics), str(metrics)))
        sys.exit(exit)
        

        
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