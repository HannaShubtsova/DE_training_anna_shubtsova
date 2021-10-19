import os

import psycopg2

pg_creds = {
    'host': '192.168.1.21'
    , 'port': '5432'
    , 'database': 'dshop'
    , 'user': 'pguser'
    , 'password': 'secret'
}


def read_from_db():
    with psycopg2.connect(**pg_creds) as pg_connection:
        cursor = pg_connection.cursor()
        cursor.execute("""select table_name FROM information_schema.tables where table_catalog = 'dshop'and table_schema ='public'""")
        result = cursor.fetchall()
        final_result = [i[0] for i in result]
        print (final_result[0])
        for table_name  in final_result:
            file_name = table_name+ '.csv'
            sql_line = 'COPY public.'+table_name+ ' TO STDOUT WITH HEADER CSV'
            with psycopg2.connect(**pg_creds) as pg_connection:
                cursor = pg_connection.cursor()
                #with open(file=os.path.join('.', 'data', file_name), mode='w') as csv_file:
                with open(os.path.join('.', file_name), 'w') as csv_file:
                    #cursor.copy_expert('COPY dshop.%s TO STDOUT WITH HEADER CSV' %table_name, csv_file)
                    cursor.copy_expert(sql_line, csv_file)
                    print('done')







if __name__ == '__main__':
    read_from_db()
