from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

class Ayarlar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 100)
        self.arayuzuAyarla()

    def arayuzuAyarla(self):
        self.setWindowTitle("Ayarlar")

        self.baslarkenkoyutema = QtWidgets.QCheckBox("Açılırken koyu temayı etkinleştir")
        self.otomatikguncelle = QtWidgets.QCheckBox("Açılırken verileri otomatik güncelle")

        self.asilLayout = QtWidgets.QVBoxLayout()
        self.asilLayout.addWidget(self.baslarkenkoyutema)
        self.asilLayout.addWidget(self.otomatikguncelle)

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

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("background-color: darkgray;")

        ileriGeriButonları = QtWidgets.QHBoxLayout()
        self.geriButon = QtWidgets.QPushButton("Geri")
        self.geriButon.setStyleSheet("background-color: white; color black;")

        self.ileriButon = QtWidgets.QPushButton("İleri")
        self.ileriButon.setStyleSheet("background-color: white; color black;")
        ileriGeriButonları.addWidget(self.geriButon)
        ileriGeriButonları.addStretch()
        ileriGeriButonları.addWidget(self.ileriButon)

        guncelleButonLayout = QtWidgets.QHBoxLayout()
        self.guncelleButon = QtWidgets.QPushButton("Güncelle")
        self.guncelleButon.setStyleSheet("background-color: white; color black;")
        guncelleButonLayout.addStretch()
        guncelleButonLayout.addWidget(self.guncelleButon)
        guncelleButonLayout.addStretch()

        self.altTaraf = QtWidgets.QHBoxLayout()
        self.etiket = QtWidgets.QLabel("2020 - Berkay Bakacak. sürüm: 2.0")
        self.altTaraf.addWidget(self.etiket)
        self.altTaraf.addStretch()
        self.koyuTema = QtWidgets.QCheckBox("Koyu tema")

        self.ayarlar = QtWidgets.QPushButton()
        self.ayarlar.setIcon(QtGui.QIcon("ayarlar.png"))

        self.altTaraf.addWidget(self.koyuTema)
        self.altTaraf.addWidget(self.ayarlar)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addLayout(guncelleButonLayout)
        layout.addLayout(ileriGeriButonları)
        layout.addWidget(self.canvas)
        layout.addLayout(self.altTaraf)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()