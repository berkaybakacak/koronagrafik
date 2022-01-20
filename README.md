# koronagrafik
PyQt5 ve Matplotlib ile ülkelerin günlük yeni koronavirüs vaka ve ölüm sayılarını gösteren program.

3.4 sürümü:
- Veritabanı güncellendi.
- Bazı metinler daha doğru ifadelerle değiştirildi.
- Ayarlar menüsündeki yazıların ekrana sığmaması hatası giderildi.
- Ayarlar menüsü açılırken "Açılışta sütun grafiği seç" seçeneğinin seçili gelmemesi hatası giderildi.
- Bazı Linux dağıtımlarında meydana gelen tasarımsal hatalar giderildi.
- macOS işletim sisteminde meydana gelen ssl doğrulaması hatası giderildi.




3.0 sürümü:
- Ülke sayısı artırıldı
- Sütun grafiği eklendi
- Ülkeler için ayrı ayrı güncelleme seçeneği eklendi
- Veritabanı güncellendi.


Program verileri https://www.worldometers.info/ adresinden kazır. Tarih bilgisini numpy yardımıyla kendisi oluşturur. Bunun için koronavirüsün ülkede görünmeye başlandığı tarih veritabanına elle girilmelidir. "hazirla.py" bu işi de üstlenmektedir.

![alt tag](örnek.png)
