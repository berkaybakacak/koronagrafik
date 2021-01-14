#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
2021 Berkay Bakacak
"""

from datetime import datetime
import sqlite3

# Veritabanı bağlantısını oluştur
bağlantı = sqlite3.connect("veriler.db")
imleç = bağlantı.cursor()

# Ülke isimleri ve koronanın ilk görülme tarihleri
ülkeler = {
    "Türkiye": "'2020-03-11'",
    "Amerika": "'2020-02-16'",
    "Kanada": "'2020-02-16'",
    "Çin": "'2020-01-23'",
    "Japonya": "'2020-02-16'",
    "Avusturya": "'2020-02-25'",
    "Belçika": "'2020-02-16'",
    "Bulgaristan": "'2020-03-08'",
    "Danimarka": "'2020-02-28'",
    "Yunanistan": "'2020-02-27'",
    "Kıbrıs": "'2020-03-10'",
    "Azerbaycan": "'2020-02-29'",
    "İngiltere": "'2020-02-16'",
    "Almanya": "'2020-02-16'",
    "Pakistan": "'2020-02-27'",
    "Fransa": "'2020-02-16'",
    "Hindistan": "'2020-02-16'",
    "Tayland": "'2020-02-16'",
    "İtalya": "'2020-02-16'",
    "Bangladeş": "'2020-03-09'",
    "Özbekistan": "'2020-03-16'"
}

# Ayarlar tablosunu oluştur
imleç.execute("CREATE TABLE IF NOT EXISTS program(grafiktipi INTEGER, koyutema INTEGER)")

# Tarihler tablosunu oluştur
imleç.execute("CREATE TABLE IF NOT EXISTS tarihler(id INTEGER PRIMARY KEY AUTOINCREMENT)")
for ülke in ülkeler:
    imleç.execute("ALTER TABLE tarihler ADD {} TEXT".format(ülke))

# Ülke tablolarını oluştur
for ülke in ülkeler:
    imleç.execute("CREATE TABLE IF NOT EXISTS " + ülke + "(bulaşma INTEGER, ölüm INTEGER)")

# Başlangıç tarihlerini kaydet ve son güncelleme tarihlerini oluştur
tarihler = ", ".join(ülkeler.values())
cümle = "INSERT INTO tarihler({}) VALUES ({})".format(", ".join(ülkeler.keys()), tarihler)
imleç.execute(cümle)

ikibinyirmibirler = ["'" + str(datetime.now()) + "'" for suAn in range(len(ülkeler.keys()))]
ikibinyirmibirler = ", ".join(ikibinyirmibirler)
cümle = "INSERT INTO tarihler({}) VALUES ({})".format(", ".join(ülkeler.keys()), ikibinyirmibirler)
imleç.execute(cümle)


imleç.execute("INSERT INTO program VALUES(0, 0)")

bağlantı.commit()