# -*- coding: utf-8 -*-
import sys, locale
import sqlite3
import numpy as np
from koronagrafik.tasarim import *
from koronagrafik.metotlar import *

"""
Koronagrafik
Son güncelleme tarihi: 14 Ocak 2021 Perşembe 17:09
Yazar: Berkay Bakacak.
"""

bağlantı = sqlite3.connect("veriler.db")
imleç = bağlantı.cursor()

try:
    locale.setlocale(locale.LC_ALL, locale="Turkish_Turkey") # Windows
except locale.Error: # Linux
    locale.setlocale(locale.LC_ALL, locale="tr_TR.utf8")

ülkeler = {
    1:"Türkiye", 2:"Amerika", 3:"Kanada", 4:"Çin", 5:"Japonya", 6:"Avusturya", 7:"Belçika", 8:"Bulgaristan",
    9:"Danimarka", 10:"Yunanistan", 11:"Kıbrıs", 12:"Azerbaycan", 13:"İngiltere", 14:"Almanya", 15:"Pakistan",
    16:"Fransa", 17:"Hindistan", 18:"Tayland", 19:"İtalya", 20:"Bangladeş", 21:"Özbekistan"
}

app = QtWidgets.QApplication(sys.argv)

pencere = MainWindow()

for ülke in ülkeler: # addItems metodu ülkeleri listeye rastgele eklediği için kullanılmamıştır.
    pencere.ulkelerListesi.addItem(ülkeler[ülke])

pencere.ulkelerListesi.currentTextChanged.connect(ulkeDegisti)
pencere.geriButon.clicked.connect(lambda: ilerigeri("geri"))
pencere.ileriButon.clicked.connect(lambda: ilerigeri("ileri"))
pencere.grafigikaydet.clicked.connect(kaydet)

pencere.ayarlar.clicked.connect(ayarlariAc)

pencere.koyuTema.stateChanged.connect(temadegisti)

pencere.geriButon.setVisible(0)
pencere.ileriButon.setText(ülkeler[2])

pencere.ulkeyiGuncelle.clicked.connect(ulkeGuncelle)
pencere.tumUlkeleriGuncelle.clicked.connect(tumUlkeleriGuncelle)

b_grafiktipi = imleç.execute("SELECT grafiktipi FROM program").fetchall()[0][0]

if b_grafiktipi == 0:
    pencere.cizgiGrafik.setChecked(True)
else:
    pencere.sutunGrafik.setChecked(True)


pencere.cizgiGrafik.toggled.connect(lambda: grafikTipiDegisti(pencere.cizgiGrafik))
pencere.sutunGrafik.toggled.connect(lambda: grafikTipiDegisti(pencere.sutunGrafik))

b_otokoyutema = imleç.execute("SELECT koyutema FROM program").fetchall()[0][0]
pencere.koyuTema.setChecked(b_otokoyutema)

if b_otokoyutema == 0:
    koronagrafik.metotlar.cizdir(ülkeler[1])


ayarlarpencere = Ayarlar()
ayarlarpencere.baslarkenkoyutema.setChecked(b_otokoyutema)

ayarlarpencere.baslarkenkoyutema.stateChanged.connect(baslarkenKoyuTema)
ayarlarpencere.baslarkensutungrafik.stateChanged.connect(baslarkenSutunGrafik)