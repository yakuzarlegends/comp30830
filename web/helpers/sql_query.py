import pymysql
import os
KIERAN_RDS_HOST = os.environ['KIERAN_RDS_HOST']
KIERAN_RDS_USER = os.environ['KIERAN_RDS_USER']
KIERAN_RDS_PW = os.environ['KIERAN_RDS_PW']


class sequeler:

    connection = pymysql.connect(host=KIERAN_RDS_HOST,
                             user=KIERAN_RDS_USER,
                             password=KIERAN_RDS_PW,
                             db='comp30830', cursorclass=pymysql.cursors.DictCursor)

    def collectData(queries):
        data = []
        with sequeler.connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
                query_data = cursor.fetchall()
                data.append(query_data)
            sequeler.connection.close()
        return data

