# -*- coding: utf-8 -*-

"""
Koronagrafik
Son güncelleme tarihi: 14 Ocak 2021 Perşembe 18:45
Yazar: Berkay Bakacak.
"""

import koronagrafik

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import datetime
import json

ülkeURL = {
    "Türkiye":["turkey", 24], "Amerika":["us", 24], "Kanada":["canada", 24], "Çin":["china", 24],
    "Japonya":["japan", 23], "Avusturya":["austria", 24], "Belçika":["belgium", 24], "Bulgaristan":["bulgaria", 22],
    "Danimarka":["denmark", 24], "Yunanistan":["greece", 22], "Kıbrıs":["cyprus", 22], "Azerbaycan":["azerbaijan", 22],
    "İngiltere":["uk", 22], "Almanya":["germany", 24], "Pakistan":["pakistan", 23], "Fransa":["france", 24],
    "Hindistan":["india", 23], "Tayland":["thailand", 23], "İtalya":["italy", 24], "Bangladeş":["bangladesh", 22],
    "Özbekistan":["uzbekistan", 22]
}

secenekler = {0:["white", "black"], 1:["black", "white"]}

def cizdir(ulkeAdi):
    secenek = koronagrafik.pencere.koyuTema.isChecked()

    başlangıç_tarihi = koronagrafik.imleç.execute("SELECT " + ulkeAdi + " FROM tarihler").fetchall()[0][0]
    günlük_yeni_vaka = koronagrafik.imleç.execute("SELECT bulaşma FROM " + ulkeAdi).fetchall()
    vaka_günleri = koronagrafik.np.arange(koronagrafik.np.datetime64(başlangıç_tarihi), len(günlük_yeni_vaka))
    günlük_ölüm = koronagrafik.imleç.execute("SELECT ölüm FROM " + ulkeAdi).fetchall()

    günlük_yeni_vaka = [m[0] for m in günlük_yeni_vaka]
    günlük_ölüm = [m[0] for m in günlük_ölüm]

    son_guncelleme_tarihi = koronagrafik.imleç.execute("SELECT " + ulkeAdi + " FROM tarihler").fetchall()[1][0]
    son_guncelleme_tarihi = datetime.datetime.strptime(son_guncelleme_tarihi, "%Y-%m-%d %H:%M:%S.%f")
    son_guncelleme_tarihi = son_guncelleme_tarihi.strftime("%d %B %Y %A %X")
    
    koronagrafik.pencere.bildiriEtiket.setText(ulkeAdi + " - son güncelleme tarihi: " + son_guncelleme_tarihi)

    koronagrafik.pencere.canvas.axes[0].cla()
    koronagrafik.pencere.canvas.axes[1].cla()

    koronagrafik.pencere.canvas.axes[0].set_title(ulkeAdi + " - günlük yeni vakalar", color=secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].set_title(ulkeAdi + " - günlük yeni ölümler", color=secenekler[secenek][1])

    if koronagrafik.pencere.sutunGrafik.isChecked() == 0:
        koronagrafik.pencere.canvas.axes[0].plot(vaka_günleri, günlük_yeni_vaka, lw=2, color="blue")
        koronagrafik.pencere.canvas.axes[1].plot(vaka_günleri, günlük_ölüm, lw=2, color="red")
    else:
        koronagrafik.pencere.canvas.axes[0].bar(vaka_günleri, günlük_yeni_vaka, 0.5, color="blue")
        koronagrafik.pencere.canvas.axes[1].bar(vaka_günleri, günlük_ölüm, 0.5, color="red")

    koronagrafik.pencere.canvas.axes[0].set_xlabel("Gün")
    koronagrafik.pencere.canvas.axes[0].set_ylabel("Vaka sayısı")

    koronagrafik.pencere.canvas.axes[1].set_xlabel("Gün")
    koronagrafik.pencere.canvas.axes[1].set_ylabel("Ölüm sayısı")

    koronagrafik.pencere.canvas.draw()

    koronagrafik.pencere.canvas.fig.tight_layout()

def guncelle(ulkeAdi):
    istek = Request("https://www.worldometers.info/coronavirus/country/" + ülkeURL[ulkeAdi][0], headers={"User-Agent": "Mozilla/5.0"})
    sayfa = urlopen(istek).read()
    sayfa = sayfa.decode()

    düzenleyici = BeautifulSoup(sayfa, "html.parser")

    ulkeScriptNo = ülkeURL[ulkeAdi][1]

    vaka_script = str(düzenleyici.find_all("script")[ulkeScriptNo])

    vaka_script = vaka_script[vaka_script.find("name: 'Daily Cases',"):]
    vaka_veriler = (vaka_script[vaka_script.find("["):vaka_script.find("]")])[1:]
    vaka_veriler = vaka_veriler.replace("null,", "")
    vaka_veriler = vaka_veriler.split(",")


    ölüm_script = str(düzenleyici.find_all("script")[ulkeScriptNo + 3])

    ölüm_script = ölüm_script[ölüm_script.find("name: 'Daily Deaths',"):]
    ölüm_veriler = (ölüm_script[ölüm_script.find("["):ölüm_script.find("]")])[1:]
    ölüm_veriler = ölüm_veriler.replace("null,", "")
    ölüm_veriler = ölüm_veriler.split(",")

    for sıfır in range(len(vaka_veriler) - len(ölüm_veriler)):
        ölüm_veriler.insert(0, 0)

    koronagrafik.imleç.execute("DELETE FROM " + ulkeAdi)

    for i, j in zip(vaka_veriler, ölüm_veriler):
        koronagrafik.imleç.execute("INSERT INTO " + ulkeAdi + " VALUES(?, ?)",(i,j))

    suAn = "'" + str(datetime.datetime.now()) + "'"
    koronagrafik.imleç.execute("UPDATE tarihler SET " + ulkeAdi + " = " + suAn + " WHERE id=2")

    koronagrafik.bağlantı.commit()

def ulkeGuncelle():
    ulke = koronagrafik.pencere.ulkelerListesi.currentText()
    koronagrafik.pencere.bildiriEtiket.setText(ulke + " - güncelleniyor...")
    guncelle(ulke)
    cizdir(ulke)

def tumUlkeleriGuncelle():
    seciliUlke = koronagrafik.pencere.ulkelerListesi.currentText()
    for ulke in koronagrafik.ülkeler:
        koronagrafik.pencere.bildiriEtiket.setText(koronagrafik.ülkeler[ulke] + " - güncelleniyor...")
        guncelle(koronagrafik.ülkeler[ulke])

    cizdir(seciliUlke)

def ilerigeri(yon):
    sira = koronagrafik.pencere.ulkelerListesi.currentIndex()

    # Listedeki seçili ülkeyi güncelle
    if yon == "ileri":
        koronagrafik.pencere.ulkelerListesi.setCurrentIndex(sira + 1)

        # Sonraki ve önceki ülkenin isimlerini düğmelere yerleştir
        if not sira > len(koronagrafik.ülkeler) - 3:
            koronagrafik.pencere.ileriButon.setText(koronagrafik.ülkeler[sira + 3])
        
        koronagrafik.pencere.geriButon.setText(koronagrafik.ülkeler[sira + 1])
    else:
        koronagrafik.pencere.ulkelerListesi.setCurrentIndex(sira - 1)

        # Sonraki ve önceki ülkenin isimlerini düğmelere yerleştir
        if not sira < 2:
            koronagrafik.pencere.geriButon.setText(koronagrafik.ülkeler[sira - 1])

        koronagrafik.pencere.ileriButon.setText(koronagrafik.ülkeler[sira + 1])

def ulkeDegisti(ulkeAdi):
    sira = koronagrafik.pencere.ulkelerListesi.currentIndex() + 1

    koronagrafik.pencere.geriButon.setVisible(1)
    koronagrafik.pencere.ileriButon.setVisible(1)

    if sira == 1:
        koronagrafik.pencere.geriButon.setVisible(0)
    elif sira == len(koronagrafik.ülkeler):
        koronagrafik.pencere.ileriButon.setVisible(0)

    if not sira > len(koronagrafik.ülkeler) - 1:
        koronagrafik.pencere.ileriButon.setText(koronagrafik.ülkeler[sira + 1])

    if not sira < 2:
        koronagrafik.pencere.geriButon.setText(koronagrafik.ülkeler[sira - 1])

    cizdir(ulkeAdi)

def grafikTipiDegisti(gt):
    cizdir(koronagrafik.pencere.ulkelerListesi.currentText())

def kaydet():
    ciktiAdi = koronagrafik.pencere.ulkelerListesi.currentText() + " - "
    if koronagrafik.pencere.sutunGrafik.isChecked():
        ciktiAdi = ciktiAdi + "Sütun grafiği"
    else:
        ciktiAdi = ciktiAdi + "Çizgi grafiği"
    
    if koronagrafik.pencere.koyuTema.isChecked():
        ciktiAdi = ciktiAdi + " - Koyu tema"
    
    ciktiAdi = ciktiAdi + ".png"

    koronagrafik.pencere.canvas.fig.savefig(ciktiAdi)

def temadegisti():
    secenek = koronagrafik.pencere.koyuTema.isChecked()

    koronagrafik.pencere.setStyleSheet("background-color: " + secenekler[secenek][0] + ";")
    koronagrafik.pencere.canvas.fig.set_facecolor(secenekler[secenek][0])

    koronagrafik.pencere.canvas.axes[0].set_facecolor(secenekler[secenek][0])
    koronagrafik.pencere.canvas.axes[1].set_facecolor(secenekler[secenek][0])

    koronagrafik.pencere.canvas.axes[0].spines["top"].set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[0].spines["left"].set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[0].spines["bottom"].set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[0].spines["right"].set_color(secenekler[secenek][1])

    koronagrafik.pencere.canvas.axes[1].spines["top"].set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].spines["left"].set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].spines["bottom"].set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].spines["right"].set_color(secenekler[secenek][1])
    
    koronagrafik.pencere.canvas.axes[0].tick_params(axis="x", colors=secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[0].tick_params(axis="y", colors=secenekler[secenek][1])

    koronagrafik.pencere.canvas.axes[1].tick_params(axis="x", colors=secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].tick_params(axis="y", colors=secenekler[secenek][1])

    koronagrafik.pencere.canvas.axes[0].xaxis.label.set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].xaxis.label.set_color(secenekler[secenek][1])

    koronagrafik.pencere.canvas.axes[0].yaxis.label.set_color(secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].yaxis.label.set_color(secenekler[secenek][1])

    koronagrafik.pencere.koyuTema.setStyleSheet("color: " + secenekler[secenek][1] + ";")
    koronagrafik.pencere.etiket.setStyleSheet("color: " + secenekler[secenek][1] + ";")
    koronagrafik.pencere.bildiriEtiket.setStyleSheet("color: " + secenekler[secenek][1] + ";")
    koronagrafik.pencere.cizgiGrafik.setStyleSheet("color: " + secenekler[secenek][1] + ";")
    koronagrafik.pencere.sutunGrafik.setStyleSheet("color: " + secenekler[secenek][1] + ";")

    cizdir(koronagrafik.pencere.ulkelerListesi.currentText())

def ayarlariAc():
    koronagrafik.ayarlarpencere.show()

def baslarkenKoyuTema():
    durum = koronagrafik.ayarlarpencere.baslarkenkoyutema.isChecked()
    koronagrafik.imleç.execute("UPDATE program SET koyutema = ?", (durum, ))
    koronagrafik.bağlantı.commit()

def baslarkenSutunGrafik():
    durum = koronagrafik.ayarlarpencere.baslarkensutungrafik.isChecked()
    koronagrafik.imleç.execute("UPDATE program SET grafiktipi = ?", (durum, ))
    koronagrafik.bağlantı.commit()