import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database: ", e)
        return None

def insert_data(conn, dates, counts, dam_ids):
    try:
        cur = conn.cursor()
        for date, count, dam_id in zip(dates, counts, dam_ids):
            cur.execute(f"INSERT INTO fish_ladder_fishcount (date, count, dam_id) VALUES ( %s, %s, %s)", (date, count, dam_id))
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        print("Error inserting data into the database: ", e)

