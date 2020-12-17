import koronagrafik

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json

ülkeler = {
    1:"Türkiye", 2:"Amerika", 3:"Kanada", 4:"Çin", 5:"Japonya", 6:"Avusturya", 7:"Belçika", 8:"Bulgaristan",
    9:"Danimarka", 10:"Yunanistan", 11:"Kıbrıs", 12:"Azerbaycan"
    }
ülke_sırası = 0
secenekler = {0:["white", "black"], 1:["black", "white"]}

def cizdir():
    secenek = koronagrafik.pencere.koyuTema.isChecked()

    başlangıç_tarihi = koronagrafik.imleç.execute("SELECT " + ülkeler[ülke_sırası] + " FROM başlangıç").fetchall()[0][0]
    günlük_yeni_vaka = koronagrafik.imleç.execute("SELECT bulaşma FROM " + ülkeler[ülke_sırası]).fetchall()
    vaka_günleri = koronagrafik.np.arange(koronagrafik.np.datetime64(başlangıç_tarihi), len(günlük_yeni_vaka))
    günlük_ölüm = koronagrafik.imleç.execute("SELECT ölüm FROM " + ülkeler[ülke_sırası]).fetchall()

    günlük_yeni_vaka = [m[0] for m in günlük_yeni_vaka]
    günlük_ölüm = [m[0] for m in günlük_ölüm]

    koronagrafik.pencere.canvas.axes[0].cla()
    koronagrafik.pencere.canvas.axes[1].cla()

    koronagrafik.pencere.canvas.axes[0].set_title(ülkeler[ülke_sırası] + " - günlük yeni vakalar", color=secenekler[secenek][1])
    koronagrafik.pencere.canvas.axes[1].set_title(ülkeler[ülke_sırası] + " - günlük yeni ölümler", color=secenekler[secenek][1])

    koronagrafik.pencere.canvas.axes[0].plot(vaka_günleri, günlük_yeni_vaka, lw=2, color="blue")
    koronagrafik.pencere.canvas.axes[1].plot(vaka_günleri, günlük_ölüm, lw=2, color="red")

    koronagrafik.pencere.canvas.axes[0].set_xlabel("Gün")
    koronagrafik.pencere.canvas.axes[0].set_ylabel("Vaka sayısı")

    koronagrafik.pencere.canvas.axes[1].set_xlabel("Gün")
    koronagrafik.pencere.canvas.axes[1].set_ylabel("Ölüm sayısı")

    koronagrafik.pencere.canvas.draw()

    koronagrafik.pencere.canvas.fig.tight_layout()

def ilerigeri(yon):
    global ülke_sırası

    if yon == "ileri" and ülke_sırası < len(ülkeler.keys()):
        ülke_sırası += 1

    elif yon == "geri" and ülke_sırası > 1:
        ülke_sırası -= 1
    
    cizdir()

def guncelle():
    print("Güncelleniyor...")
    ülkeURL = {
        "Türkiye":["turkey"], "Amerika":["us"], "Kanada":["canada"], "Çin":["china"],
        "Japonya":["japan"], "Avusturya":["austria"], "Belçika":["belgium"], "Bulgaristan":["bulgaria"],
        "Danimarka":["denmark"], "Yunanistan":["greece"], "Kıbrıs":["cyprus"], "Azerbaycan":["azerbaijan"]
        }

    for ülke in ülkeURL.keys():
        istek = Request("https://www.worldometers.info/coronavirus/country/" + ülkeURL[ülke][0], headers={"User-Agent": "Mozilla/5.0"})
        sayfa = urlopen(istek).read()
        sayfa = sayfa.decode()

        düzenleyici = BeautifulSoup(sayfa, "html.parser")

        if ülke == "Japonya":
            vaka_script = str(düzenleyici.find_all("script")[23])
        elif ülke == "Bulgaristan" or ülke == "Yunanistan" or ülke == "Kıbrıs" or ülke == "Azerbaycan":
            vaka_script = str(düzenleyici.find_all("script")[22])
        else:
            vaka_script = str(düzenleyici.find_all("script")[24])

        vaka_script = vaka_script[vaka_script.find("name: 'Daily Cases',"):]
        vaka_veriler = (vaka_script[vaka_script.find("["):vaka_script.find("]")])[1:]
        vaka_veriler = vaka_veriler.replace("null,", "")
        vaka_veriler = vaka_veriler.split(",")

        if ülke == "Japonya":
            ölüm_script = str(düzenleyici.find_all("script")[26])
        elif ülke == "Bulgaristan" or ülke == "Yunanistan" or ülke == "Kıbrıs" or ülke == "Azerbaycan":
            ölüm_script = str(düzenleyici.find_all("script")[25])
        else:
            ölüm_script = str(düzenleyici.find_all("script")[27])
            
        ölüm_script = ölüm_script[ölüm_script.find("name: 'Daily Deaths',"):]
        ölüm_veriler = (ölüm_script[ölüm_script.find("["):ölüm_script.find("]")])[1:]
        ölüm_veriler = ölüm_veriler.replace("null,", "")
        ölüm_veriler = ölüm_veriler.split(",")

        for sıfır in range(len(vaka_veriler) - len(ölüm_veriler)):
            ölüm_veriler.insert(0, 0)

        koronagrafik.imleç.execute("DELETE FROM " + ülke)

        for i, j in zip(vaka_veriler, ölüm_veriler):
            koronagrafik.imleç.execute("INSERT INTO " + ülke + " VALUES(?, ?)",(i,j))
    
    koronagrafik.bağlantı.commit()
    print("Güncellendi.")

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

    cizdir()

def ayarlariac():
    koronagrafik.ayarlarpencere.show()

def otomatikguncelleSecenek():
    durum = koronagrafik.ayarlarpencere.otomatikguncelle.isChecked()
    koronagrafik.imleç.execute("UPDATE program SET otomatikguncelle = ?", (durum, ))
    koronagrafik.bağlantı.commit()

def koyutemaSecenek():
    durum = koronagrafik.ayarlarpencere.baslarkenkoyutema.isChecked()
    koronagrafik.imleç.execute("UPDATE program SET koyutema = ?", (durum, ))
    koronagrafik.bağlantı.commit()