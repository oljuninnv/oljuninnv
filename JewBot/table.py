import sqlite3
from bs4 import BeautifulSoup as bs


db = sqlite3.connect("info",check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS price(магазин TEXT NOT NULL,категория продуктов TEXT NOT NULL,название товара TEXT NOT NULL,изображение BLOB ,цена  REAL)")
