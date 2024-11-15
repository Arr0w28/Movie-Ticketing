import psycopg2
import sys
sys.path.append('C:/Users/smoha/Documents/VIT/SEM 5/AWS/Own')
from utils.aws_config import DATABASE


def get_db_connection():
    # Access the database config for 'mohan
    config = DATABASE['mohan']
    conn = psycopg2.connect(
        host=config['movieticket.c3cwmaq8m96y.ap-south-1.rds.amazonaws.com'],
        port=config['5432'],
        user=config['mohan'],
        password=config['mohan2005vitcc'],
        database=config['movieticket']
    )
    return conn



