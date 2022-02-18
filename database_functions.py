import os
import glob
import csv
import time
import mysql.connector as mysql
from pprint import pprint
import logging
from decouple import config



logging.basicConfig(filename='./logfile',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger()


def create_tables_database():
    logger.info('Creando tabla en la base de datos')
    db = mysql.connect(
        host=config('MYSQL_HOST'),
        user=config('MYSQL_USER'),
        passwd=config('MYSQL_PASSWORD'),
        database=config('MYSQL_DATABASE')
    )

    try:
        cursor = db.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS data (
          played_at DATETIME, 
          artist VARCHAR(255),
          track VARCHAR(255)
          )""")
    except Exception as e:
        logger.error(f'Error creando tablas en DB: {e}')

    return



def insert_database(played_at, artist, track):
    db = mysql.connect(
        host=config('MYSQL_HOST'),
        user=config('MYSQL_USER'),
        passwd=config('MYSQL_PASSWORD'),
        database=config('MYSQL_DATABASE')
    )
    try:
        logger.info(f"Insertando en DB: played_at: {played_at}, artist: {artist}, track: {track}")
        cursor = db.cursor()
        query = "INSERT INTO data (played_at, artist, track) VALUES (%s, %s, %s)"
        values = (played_at,
                    artist,
                    track)
        cursor.execute(query, values)
        db.commit()

    except Exception as e:
        logger.error(f'Error al insertar datos en DB: {e}')
    return
