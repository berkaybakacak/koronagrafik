import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import re

def verileriGetir(ülke):
    global vaka_başlangıç_tarihi
    global ölüm_başlangıç_tarihi

    global vaka_günleri
    global vakalar

    global ölüm_günleri
    global ölümler

    bağlantı = sqlite3.connect("veriler.db")
    imleç = bağlantı.cursor()

    vaka_başlangıç_tarihi = imleç.execute("SELECT " + ülke + " FROM başlangıç").fetchall()[0][0]
    ölüm_başlangıç_tarihi = imleç.execute("SELECT " + ülke + " FROM başlangıç").fetchall()[1][0]
    
    vakalar = imleç.execute("SELECT bulaşma FROM " + ülke).fetchall()
    vaka_günleri = np.arange(np.datetime64(vaka_başlangıç_tarihi), len(vakalar))
    
    ölümler = imleç.execute("SELECT ölüm FROM " + ülke).fetchall()
    ölüm_günleri = np.arange(np.datetime64(ölüm_başlangıç_tarihi), len(ölümler))

    bağlantı.close()

def çiz():
    plt.style.use("dark_background")

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 7))

    axes[0].plot(vaka_günleri, vakalar)
    axes[0].set_title("Günlük yeni vaka sayısı")
    axes[0].set_xlabel("Gün")
    axes[0].set_ylabel("Vaka sayısı")   

    axes[1].plot(ölüm_günleri, ölümler, color="red")
    axes[1].set_title("Günlük ölüm sayısı")
    axes[1].set_xlabel("Gün")
    axes[1].set_ylabel("Ölüm sayısı")

    fig.tight_layout()
    plt.show()

def düzelt(ülkeismi):
    düzeltme = {
        "türkiye": {"turkiye", "türkiy", "türkye", "turkey", "tr"},
        "amerika": {"america", "united states", "united states america", "united states of america", "usa"},
        "kanada": {"canada", "kanda", "canda", "ca"}
    }

    ülkeismi = ülkeismi.lower()
    ülkeismi = ülkeismi.strip()
    ülkeismi = re.sub('[^A-Za-zçöüğşı ]+', '', ülkeismi)

    for ülke in düzeltme.keys():
        if ülkeismi in düzeltme[ülke]:
            ülkeismi = ülke

    return ülkeismi

def main():
    while True:
        ülke = input("Verilerini görmek istediğiniz ülkenin ismini yazın(çıkmak için 'k'): ")
        if ülke == "k":
            break
        
        ülke = düzelt(ülke)

        try:
            verileriGetir(ülke)
            çiz()
        except:
            print("Ülke bulunamadı.")

if __name__ == "__main__":
    main()
