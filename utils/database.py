import psycopg2
from utils.aws_config import DATABASE

def get_db_connection():
    connection = psycopg2.connect(
        host=DATABASE['movieticket.c3cwmaq8m96y.ap-south-1.rds.amazonaws.com'],
        port=DATABASE['5432'],
        user=DATABASE['mohan'],
        password=DATABASE['mohan2005vitcc'],
        dbname=DATABASE['movieticket']
    )
    return connection
