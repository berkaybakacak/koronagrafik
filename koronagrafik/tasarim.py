# -*- coding: utf-8 -*-

"""
Koronagrafik
Son güncelleme tarihi: 21 Ocak 2022 Cuma 01:19
Yazar: Berkay Bakacak.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

class Ayarlar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 100)
        self.arayuzuAyarla()

    def arayuzuAyarla(self):
        self.setWindowTitle("Ayarlar")
        self.setStyleSheet("background-color: #ececeb;")

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
        self.setWindowTitle("Koronavirüs günlük yeni vaka/yeni ölü grafiği")
        self.setStyleSheet("background-color: #ececeb;")

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.fig.set_facecolor("#ececeb")
        self.canvas.axes[0].set_facecolor("#ececeb")
        self.canvas.axes[1].set_facecolor("#ececeb")

        self.butonStiller = {1:["""
        QPushButton {
            color: black;
            background-color: white;
            border-radius: 5px;
            width: 110px;
            height: 20px;
            border: 1px solid darkgray;
        }

        QPushButton:pressed {
            background-color: gray;
            color: white;
        }
        """,
        """
        QPushButton {
            color: white;
            background-color: darkgray;
            border-radius: 5px;
            width: 110px;
            height: 20px;
            border: 1px solid white;
        }

        QPushButton:pressed {
            background-color: gray;
            color: black;
        }
        """]}
        self.butonStiller[2] = []
        self.butonStiller[2].append(self.butonStiller[1][0].replace("width: 110px;", "width: 200px;"))
        self.butonStiller[2].append(self.butonStiller[1][1].replace("width: 110px;", "width: 200px;"))



        self.comboBoxStil = ["""
        QComboBox {
            width: 110px;
            height: 20px;
            border-radius: 5px;
            border: 1px solid darkgray;
            color: black;
            background-color: white;
        }
        """,
        """
        QComboBox {
            width: 110px;
            height: 20px;
            border-radius: 5px;
            border: 1px solid white;
            color: white;
            background-color: black;
        }
        """]

        ustBolum = QtWidgets.QHBoxLayout()


        self.geriButon = QtWidgets.QPushButton("Geri")
        self.geriButon.setStyleSheet(self.butonStiller[1][0])
        ustBolum.addWidget(self.geriButon)


        self.ulkelerListesi = QtWidgets.QComboBox()
        self.ulkelerListesi.setStyleSheet(self.comboBoxStil[0])
        ustBolum.addWidget(self.ulkelerListesi)

        self.ileriButon = QtWidgets.QPushButton("İleri")
        self.ileriButon.setStyleSheet(self.butonStiller[1][0])
        ustBolum.addWidget(self.ileriButon)

        self.bildiriEtiket = QtWidgets.QLabel("Son güncelleme tarihi: ")
        ustBolum.addWidget(self.bildiriEtiket)

        ustBolum.addStretch()

        self.cizgiGrafik = QtWidgets.QRadioButton("Çizgi grafik")
        self.cizgiGrafik.setStyleSheet("background-color: #ececeb; color black;")

        self.sutunGrafik = QtWidgets.QRadioButton("Sütun grafik")
        self.sutunGrafik.setStyleSheet("background-color: #ececeb; color black;")

        ustBolum.addWidget(self.cizgiGrafik)
        ustBolum.addWidget(self.sutunGrafik)

        self.ulkeyiGuncelle = QtWidgets.QPushButton("Ülkeyi güncelle")
        self.ulkeyiGuncelle.setStyleSheet(self.butonStiller[1][0])
        ustBolum.addWidget(self.ulkeyiGuncelle)

        self.grafigikaydet = QtWidgets.QPushButton("Kaydet")
        self.grafigikaydet.setStyleSheet(self.butonStiller[1][0])
        ustBolum.addWidget(self.grafigikaydet)

        guncelleButonLayout = QtWidgets.QHBoxLayout()
        self.tumUlkeleriGuncelle = QtWidgets.QPushButton("Tüm ülkelerin verilerini güncelle")
        self.tumUlkeleriGuncelle.setStyleSheet(self.butonStiller[2][0])
        

        guncelleButonLayout.addStretch()
        guncelleButonLayout.addWidget(self.tumUlkeleriGuncelle)
        guncelleButonLayout.addStretch()

        self.altTaraf = QtWidgets.QHBoxLayout()
        self.etiket = QtWidgets.QLabel("2021 - 2022. Berkay Bakacak. sürüm: 3.4")
        self.altTaraf.addWidget(self.etiket)
        self.altTaraf.addStretch()
        self.koyuTema = QtWidgets.QCheckBox("Koyu tema")

        self.ayarlar = QtWidgets.QPushButton()
        self.ayarlar.setIcon(QtGui.QIcon("ayarlar.png"))
        self.ayarlar.setStyleSheet("border-radius: 100%; background-color: transparent;")

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
