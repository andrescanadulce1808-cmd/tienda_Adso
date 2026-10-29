import os
from contextlib import contextmanager
import pymysql
from pymysql.constants import CLIENT
from dotenv import load_dotenv
load_dotenv()

@contextmanager
def conectar():
    conexion = pymysql.connect(
        host=os.getenv('DB_HOST','localhost'),
        port=int(os.getenv('DB_PORT','3306')),
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.getenv('DB_NAME','tienda_adso'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        connect_timeout=10,
        # rowcount de un UPDATE cuenta las filas ENCONTRADAS, no solo las que cambian.
        # Sin esto, actualizar con los mismos valores daría un falso 404.
        client_flag=CLIENT.FOUND_ROWS,
    )
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()