import psycopg2
from utils.aws_config import DATABASE

def get_db_connection():
    connection = psycopg2.connect(
        host=DATABASE['mohan']['movieticket.c3cwmaq8m96y.ap-south-1.rds.amazonaws.com'],
        port=DATABASE['mohan']['5432'],
        user=DATABASE['mohan']['mohan'],
        password=DATABASE['mohan']['mohan2005vitcc'],
        dbname=DATABASE['mohan']['movieticket']
    )
    return connection
