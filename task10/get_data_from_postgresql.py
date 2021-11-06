import os
import psycopg2
import json
import os
from datetime import date
from hdfs import InsecureClient  # library docs https://hdfscli.readthedocs.io/en/latest/index.html

pg_creds = {
    'host': '192.168.1.21'
    , 'port': '5432'
    , 'database': 'dshop_bu'
    , 'user': 'pguser'
    , 'password': 'secret'
}

client = InsecureClient(f'http://127.0.0.1:50070/', user='user')


def get_tables_list():
    with psycopg2.connect(**pg_creds) as pg_connection:
        cursor = pg_connection.cursor()
        cursor.execute(
            """select table_name FROM information_schema.tables where table_catalog = 'dshop_bu'and table_schema 
            ='public'""")
        result = cursor.fetchall()
        final_result = [i[0] for i in result]
        final_result.sort()
        print(final_result)
        return final_result


def read_from_db(st):
    with psycopg2.connect(**pg_creds) as pg_connection:
        file_name = '/test/' + date.today() + '/' + st + '.csv'
        sql_line = 'COPY public.' + st + ' TO STDOUT WITH HEADER CSV'
        cursor = pg_connection.cursor()
        with client.write(file_name, ) as csv_file:
            cursor.copy_expert('sql_line', csv_file)



if __name__ == '__main__':
    print(get_tables_list())
    for i in get_tables_list():
        read_from_db(i)
        print(i)
