# python 3 
import yaml
import os
import sqlite3

with open('.creds.yml') as f:
    config = yaml.load(f)

SLACK_API_TOKEN = config['slack']['token']
INSTAGRAM_API_KEY = config['instagram']['key']
INSTAGRAM_API_SECRET = config['instagram']['secret']

#################################################################
# POPULATE CREDS TOO LOCAL SQLITE (AIRFLOW BACKEND)
#################################################################

def get_slack_api_secret():
	print (' slack_api_token = ', slack_api_token)
	return slack_api_token

def delete_existing_connections(cursor):
    sql = """
        DELETE FROM "connection"
        --WHERE conn_id IN ('aws_default'); 
    """

    cursor.execute(sql)

def insert_slack_default_conn(cursor):
    sql = """
        INSERT INTO connection  
        ( conn_id, conn_type, host, schema, login, password, port, extra, is_encrypted, is_extra_encrypted)
        VALUES('slack_default', 'slack', '', '', '{DEFAULT_SLACK_API_TOKEN}', '{DEFAULT_SLACK_API_TOKEN2}', '', '', 0, 0);
        """.format(
            DEFAULT_SLACK_API_TOKEN=SLACK_API_TOKEN,
            DEFAULT_SLACK_API_TOKEN2=SLACK_API_TOKEN
            )
    cursor.execute(sql)

def insert_instagram_default_conn(cursor):
    sql = """
        INSERT INTO connection  
        ( conn_id, conn_type, host, schema, login, password, port, extra, is_encrypted, is_extra_encrypted)
        VALUES('instagram_default', 'instagram', '', '', '{DEFAULT_INSTAGRAM_API_KEY}', '{DEFAULT_INSTAGRAM_API_SECRET}', '', '', 0, 0);
        """.format(
            DEFAULT_INSTAGRAM_API_KEY=INSTAGRAM_API_KEY,
            DEFAULT_INSTAGRAM_API_SECRET=INSTAGRAM_API_SECRET
            )
    cursor.execute(sql)



def insert_spark_conn(cursor):
    sql = """INSERT INTO connection
        (conn_id, conn_type, host, schema, login, password, port, extra, is_encrypted, is_extra_encrypted)
        VALUES('spark_default', '', '', '', '', '', '', '{{"SPARK_HOME":"{SPARK_HOME}"}}', 0, 0);
        """.format(
            SPARK_HOME='/Users/' + os.getlogin() + '/spark'
    )

    cursor.execute(sql)

def main(db_file):
    # config 
    conn = sqlite3.connect(db_file)
    try: 

        cursor = conn.cursor()
        print("Deleting all existing connections")
        delete_existing_connections(cursor)
        conn.commit()

        print('Inserting slack credentials')
        insert_slack_default_conn(cursor)
        conn.commit()

        print('Inserting instagram credentials')
        insert_instagram_default_conn(cursor)
        conn.commit()

        print('Inserting spark config')
        insert_spark_conn(cursor)
        conn.commit()

    except Exception as e:
        print ('Insert credentials failed.. ')
        print (e)

if __name__ == '__main__':
    main('airflow.db')
