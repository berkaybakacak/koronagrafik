import sqlite3

bağlantı = sqlite3.connect("veriler.db")
imleç = bağlantı.cursor()

imleç.execute("CREATE TABLE IF NOT EXISTS program(otomatikguncelle INTEGER, koyutema INTEGER)")

imleç.execute("""CREATE TABLE IF NOT EXISTS başlangıç
(Türkiye TEXT, Amerika TEXT, Kanada TEXT, Çin TEXT, Japonya TEXT, Avusturya TEXT,
Belçika TEXT, Bulgaristan TEXT, Danimarka TEXT, Yunanistan TEXT, Kıbrıs TEXT,
Azerbaycan TEXT)""")

imleç.execute("CREATE TABLE IF NOT EXISTS Türkiye(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Amerika(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Kanada(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Çin(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Japonya(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Avusturya(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Belçika(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Bulgaristan(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Danimarka(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Yunanistan(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Kıbrıs(bulaşma INTEGER, ölüm INTEGER)")
imleç.execute("CREATE TABLE IF NOT EXISTS Azerbaycan(bulaşma INTEGER, ölüm INTEGER)")

imleç.execute("INSERT INTO program VALUES(0, 0)")

imleç.execute("""INSERT INTO başlangıç VALUES
('2020-03-11', '2020-02-16', '2020-02-16', '2020-01-23', '2020-02-16', '2020-02-25', '2020-02-16', '2020-03-08',
'2020-02-28', '2020-02-27', '2020-03-10', '2020-02-29')""")

bağlantı.commit()