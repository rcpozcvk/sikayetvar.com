#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_table import Table, Col
import mysql.connector

class ItemTable(Table):
    user = Col('Kullanıcı')
    title = Col('Başlık')
    text = Col('Metin')
    border = True

class Item(object):
    def __init__(self, user, title, text):
        self.user = user
        self.title = title
        self.text = text

def get_cnx():
	cnx = mysql.connector.connect(user = "root", password = "", host = "127.0.0.1", port = 3306, database = "Complaints")
	return cnx


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def getApp():
	cnx = get_cnx() # veritabanı bağlantısı
	cur = cnx.cursor(dictionary=True)

	sql = "SELECT * FROM complaints"
	cur.execute(sql)
	rows = cur.fetchall() # complaints tablosundaki bütün satırları çekiyoruz
	
	items = [Item(row["Kullanıcı"], row["Başlık"], row["Metin"]) for row in rows] # her bir şikayeti yukarıda oluşturduğumuz Item sınıfının yapısına dönüştürüyoruz. bunu aşağıda tablo yapmak için kullanacağız.

	table = ItemTable(items) # ItemTable sınıfı Flask'in özel bir sınıfı. veritabanından çekeceğimiz bütün satırların html tablosu halinde, yani daha düzenli bir formda gözükmesini sağlayacak.

	return table.__html__()


if __name__ == '__main__':
	app.run()