#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import requests
from bs4 import BeautifulSoup

complaints = []
for i in range(2): # 10 sayfalık veri çekiliyor, arttırılabilir
	print (i+1, ". sayfa")
	url = "https://www.sikayetvar.com/turk-telekom?page=" + str(i+1)
	page = requests.get(url) # web sayfası yükleniyor
	soup = BeautifulSoup(page.content, 'html.parser') # html kodu alınıyor.

	articles = soup.find("div", {"class": "brandsearch-cards clearfix"}).findAll("article") # sayfadaki her şikayet için bir kart var.
	for article in articles: # kartları dolaşıyoruz
		try: 
			article_url = "https://www.sikayetvar.com" + article.find("h5").find("a")["href"] # kartın üstüne tıklandığında açılan sayfanın url'i bu
			article_page = requests.get(article_url) # kartın üzerine tıklıyoruz.
			article_soup = BeautifulSoup(article_page.content, 'html.parser') # açılan şikayet sayfasının html kodu

			user = article_soup.find("span", {"class": "profile-name"}).get_text() # şikayet sayfasında kullanıcı adı
			title = article_soup.find("h1").get_text() # şikayet sayfasında şikayet başlığı
			text = article_soup.find("div", {"class": "card-text"}).get_text() # şikayet sayfasında şikayet metni

			complaints.append((user, title, text)) # bu 3 bilgiyi bir tuple halinde complaints listesine ekliyoruz
		except: 
			continue


def get_cnx(): # veritabanı bağlantısı için fonksiyon
	cnx = mysql.connector.connect(user = "root", password = "", host = "127.0.0.1", port = 3306, database = "Complaints")
	return cnx

cnx = get_cnx() 
cur = cnx.cursor(dictionary=True)

sql_delete = "DROP TABLE complaints"
sql_create = "CREATE TABLE complaints (ID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, Kullanıcı varchar(20) NOT NULL, Başlık varchar(200) NOT NULL, Metin varchar(10000) NOT NULL)"

try: # eğer complaints diye bir tabklo veritabanında varsa, siliyoruz.
	cur.execute(sql_delete)
except: 
	pass
 
cur.execute(sql_create) # yeni complaints tablosunu oluşturuyoruz.


sql_insert = "INSERT INTO complaints (Kullanıcı, Başlık, Metin) VALUES (%s, %s, %s)"

for complaint in complaints: # complaints listesindeki her bir şikayeti veritabanında oluşturduğumuz tabloya kaydediyoruz.
	try: 
		cur.execute(sql_insert, complaint)
	except: 
		pass
	
	
cnx.commit() # veritabanında yaptığımız değişiklikleri kaydediyoruz.
cur.close() 
cnx.close() 






