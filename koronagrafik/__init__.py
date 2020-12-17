import sys
import sqlite3
import numpy as np
from koronagrafik.tasarim import *
from koronagrafik.metotlar import *

bağlantı = sqlite3.connect("veriler.db")
imleç = bağlantı.cursor()

app = QtWidgets.QApplication(sys.argv)

pencere = MainWindow()

pencere.geriButon.clicked.connect(lambda: ilerigeri("geri"))
pencere.ileriButon.clicked.connect(lambda: ilerigeri("ileri"))
pencere.guncelleButon.clicked.connect(guncelle)

pencere.koyuTema.stateChanged.connect(temadegisti)
pencere.ayarlar.clicked.connect(ayarlariac)

ayarlarpencere = Ayarlar()

otoguncelle = imleç.execute("SELECT otomatikguncelle FROM program").fetchall()[0][0]
ayarlarpencere.otomatikguncelle.setChecked(otoguncelle)

otokoyutema = imleç.execute("SELECT koyutema FROM program").fetchall()[0][0]
ayarlarpencere.baslarkenkoyutema.setChecked(otokoyutema)

ayarlarpencere.otomatikguncelle.stateChanged.connect(otomatikguncelleSecenek)
ayarlarpencere.baslarkenkoyutema.stateChanged.connect(koyutemaSecenek)

ilerigeri("ileri")

if otoguncelle == 1:
    guncelle()

pencere.koyuTema.setChecked(otokoyutema)