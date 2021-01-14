# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

"""
Koronagrafik
Son güncelleme tarihi: 14 Ocak 2021 Perşembe 17:19
Yazar: Berkay Bakacak.
"""

class Ayarlar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 100)
        self.arayuzuAyarla()

    def arayuzuAyarla(self):
        self.setWindowTitle("Ayarlar")

        self.baslarkenkoyutema = QtWidgets.QCheckBox("Açılırken koyu temayı etkinleştir")
        self.baslarkensutungrafik = QtWidgets.QCheckBox("Açılışta sütun grafiği seç")

        self.asilLayout = QtWidgets.QVBoxLayout()
        self.asilLayout.addWidget(self.baslarkenkoyutema)
        self.asilLayout.addWidget(self.baslarkensutungrafik)

        self.setLayout(self.asilLayout)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 6))
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(1000, 700)
        self.setWindowTitle("Koronavirüs günlük bulaşma/ölüm grafiği")

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        ustBolum = QtWidgets.QHBoxLayout()

        self.geriButon = QtWidgets.QPushButton("Geri")
        self.geriButon.setStyleSheet("background-color: white; color black;")
        ustBolum.addWidget(self.geriButon)

        self.ulkelerListesi = QtWidgets.QComboBox()
        self.ulkelerListesi.setStyleSheet("background-color: white; color black;")

        ustBolum.addWidget(self.ulkelerListesi)

        self.ileriButon = QtWidgets.QPushButton("İleri")
        self.ileriButon.setStyleSheet("background-color: white; color black;")
        
        ustBolum.addWidget(self.ileriButon)

        self.bildiriEtiket = QtWidgets.QLabel("Son güncelleme tarihi: ")
        ustBolum.addWidget(self.bildiriEtiket)

        ustBolum.addStretch()

        self.cizgiGrafik = QtWidgets.QRadioButton("Çizgi grafik")
        self.cizgiGrafik.setStyleSheet("background-color: white; color black;")

        self.sutunGrafik = QtWidgets.QRadioButton("Sütun grafik")
        self.sutunGrafik.setStyleSheet("background-color: white; color black;")

        ustBolum.addWidget(self.cizgiGrafik)
        ustBolum.addWidget(self.sutunGrafik)

        self.ulkeyiGuncelle = QtWidgets.QPushButton("Ülkeyi güncelle")
        self.ulkeyiGuncelle.setStyleSheet("background-color: white; color black;")
        ustBolum.addWidget(self.ulkeyiGuncelle)

        self.grafigikaydet = QtWidgets.QPushButton("Kaydet")
        self.grafigikaydet.setStyleSheet("background-color: white; color black;")
        ustBolum.addWidget(self.grafigikaydet)

        guncelleButonLayout = QtWidgets.QHBoxLayout()
        self.tumUlkeleriGuncelle = QtWidgets.QPushButton("Tüm ülkeleri güncelle")
        self.tumUlkeleriGuncelle.setStyleSheet("background-color: white; color black;")
        guncelleButonLayout.addStretch()
        guncelleButonLayout.addWidget(self.tumUlkeleriGuncelle)
        guncelleButonLayout.addStretch()

        self.altTaraf = QtWidgets.QHBoxLayout()
        self.etiket = QtWidgets.QLabel("2021 - Berkay Bakacak. sürüm: 3.0")
        self.altTaraf.addWidget(self.etiket)
        self.altTaraf.addStretch()
        self.koyuTema = QtWidgets.QCheckBox("Koyu tema")

        self.ayarlar = QtWidgets.QPushButton()
        self.ayarlar.setIcon(QtGui.QIcon("ayarlar.png"))

        self.altTaraf.addWidget(self.koyuTema)
        self.altTaraf.addWidget(self.ayarlar)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(guncelleButonLayout)
        layout.addLayout(ustBolum)
        layout.addWidget(self.canvas)
        layout.addLayout(self.altTaraf)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()