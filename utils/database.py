import psycopg2
from utils.aws_config import DATABASE

def get_db_connection():
    connection = psycopg2.connect(
        host=DATABASE['host'],
        port=DATABASE['port'],
        user=DATABASE['mohan'],
        password=DATABASE['Mohan2005vitcc'],
        dbname=DATABASE['cinema-db']
    )
    return connection
