import sqlite3  #SQL'i dahil ediyoruz
import time
con=sqlite3.connect("StudentFile2.db")   #Database oluşturduk
cursor=con.cursor()

isimler_list=[]     #Metinde bulunan toplu isimleri topluca buraya kaydediyoruz
vizeler_list=[]     #Metinden gelen vize notlarını topluca buraya kaydediyoruz
finaller_list=[]    #Metinden gelen final notlarını topluca buraya kaydediyoruz
projeler_list=[]    #Metinden gelen proje notları burada
ortalama_list=[]    #Metinden gelen vize+final+projelerin belirli yüzdesi ile hesaplanarak ortalamasını buraya kaydediyoruz


class DataBase():      #SQL dosya oluşturma-Veri Ekleme-Veri Kontrol İşlemleri
    def baglanti_olustur(self):
        cursor.execute("create table if not exists exam_note(Name TEXT,Vize INT,final INT,Proje INT,ort INT)")
        con.commit()

    def veri_ekleme(self,name,vize,final,proje,ort):
        cursor.execute("insert into exam_note values(?,?,?,?,?)",(name,vize,final,proje,ort))
        print("Veri eklemeniz başarıyla gerçekleşti")
        con.commit()

    def tumverileri_goster(self):
        cursor.execute("select * from exam_note")
        liste=cursor.fetchall()
        print("-------------------Data Base----------------")
        for x in liste:
            print(x)

    def secili_veri(self,name):
        cursor.execute("select * from exam_note where Name=?",(name,))
        liste=cursor.fetchall()
        for x in liste:
            print(x)

    def vize_degistirme(self):
        name=input("Lutfen ogrencinin ismini ve soyadini giriniz: ")
        if(self.secili_veri(name)!=" "):
            vize_notu=int(input("Lutfen yeni vize notunu giriniz: "))
            cursor.execute("update exam_note set vize=? where name=?", (vize_notu, name)) #isimden ulaşıp vizeyi değiştirdik
            print("Yeni Vize Notu {} olup başarıyla degistirilmistir".format(vize_notu))
        else:
            print("Girilen İsim/Soyisime göre öğrenci bulunamadı.Lütfen tekrar gözden geçiriniz!")
        con.commit()

    def final_degistirme(self):
        name=input("Lutfen ogrencinin ismini ve soyadini giriniz: ")
        if(self.secili_veri(name)!=" "):
            final_notu=int(input("Lutfen yeni final notunu giriniz: "))
            cursor.execute("update exam_note set Final=? where name=?", (final_notu, name)) #isimden ulaşıp finali değiştirdik
            print("Yeni Vize Notu {} olup başarıyla degistirilmistir".format(final_notu))
        else:
            print("Girilen İsim/Soyisime göre öğrenci bulunamadı.Lütfen tekrar gözden geçiriniz!")
        con.commit()

    def proje_degistirme(self):
        name=input("Lutfen ogrencinin ismini ve soyadini giriniz: ")
        if(self.secili_veri(name)!=" "):
            proje_notu=int(input("Lutfen yeni proje notunu giriniz: "))
            cursor.execute("update exam_note set Proje=? where name=?", (proje_notu, name)) #isimden ulaşıp proje değiştirdik
            print("Yeni Vize Notu {} olup başarıyla degistirilmistir".format(proje_notu))
        else:
            print("Girilen İsim/Soyisime göre öğrenci bulunamadı.Lütfen tekrar gözden geçiriniz!")
        con.commit()



def dosya_verileri():       #Metindeki tüm verilerin işlemlerini burada yapıyoruz
    with open("dosya.txt","r",encoding="utf-8") as source:
        for x in source:
            x=x[:-1]    #Boşlukları sildik
            x=x.split(",")   #isim-vize-final-proje ayırmasını yaptık
            isimler=x[0]     #isimler 0.indextekileri oluştruyor 'Abdullah Balcan','80','100','95'
            vize=int(x[1])   #vize notlar
            final=int(x[2])  #final notlar
            proje=int(x[3])  #proje notlar
                                              #Baştaki listelere atamasını yaptık
            isimler_list.append(isimler)
            vizeler_list.append(vize)
            finaller_list.append(final)
            projeler_list.append(proje)

            genel_ort = (vize * 3 / 10) + (final * 5 / 10) + (proje* 2 / 10) #Ortalama Hesaplatma
            ortalama_list.append(genel_ort)

dosya_verileri()  #Dosya verilerini çağırıp içindeki  işlemleri yaptık

database=DataBase()
database.baglanti_olustur()

                        #Bu kısımda dosyamızdaki tüm verileri database'imize aktardık
"""sayac=0
while (sayac<len(isimler_list)):            #Bu kısımda ayıkladığımız metindeki tüm verileri databasimize aktarıyoruz
    database.veri_ekleme(isimler_list[sayac],vizeler_list[sayac],finaller_list[sayac],projeler_list[sayac],ortalama_list[sayac])
    sayac+=1

database.tumverileri_goster()
"""



print("-----------------DATABASE--------------------\n1-Tum Ogrencilerin Verileri\n2-Yeni Veri Girişi\n3-Seçili Öğrenci Bilgisi\n4-Vize Notu Değiştirme\n5-Final Notu Değiştirme\n6-Proje Notu Değiştirme")

while True:
    islem=input("Lutfen bir işlem seçiniz: ")
    if(islem=="1"):
        database.tumverileri_goster()
    elif(islem=="2"):
        name=input("Lutfen yeni öğrencinin ismini ve soyadını boşluk bırakarak giriniz: ")
        vize_not=int(input("Lutfen {}'in vize notunu giriniz: ".format(name)))
        final_not=int(input("Lutfen {}'in final notunu giriniz: ".format(name)))
        proje_not=int(input("Lutfen {}'in proje notunu giriniz: ".format(name)))
        if(vize_not<0 or vize_not>100 and final_not<0 or final_not>100 and proje_not<0 or proje_not>100 ):
            print("Not sistemimiz 0 ila 100 arası olmaktaıdr. Girilen notlar gerekli şartı sağlamamıştır.Lütfen notları tekrardan gözden geçirin!")
        else:
            ort = (vize_not * 3 / 10) + (final_not * 5 / 10) + (proje_not * 2 / 10)
            database.veri_ekleme(name,vize_not,final_not,proje_not,ort)
    elif(islem=="3"):
        ogrenci=input("Lutfen öğrencinin ad ve soyadını giriniz: ")
        if(database.secili_veri(ogrenci)!=" "):                                     #Database kontrol işlemi yaptık
            print("İstenilen Öğrencinin Bilgileri Getiriliyor...")
            time.sleep(1)
            database.secili_veri(ogrenci)
        else:
            print("Girilen Öğrenciye Ait Bilgi Bulunmamıştor.Lütfen tekrar gözden geçiriniz!")


    elif(islem=="4"):
        database.vize_degistirme()
    elif(islem=="5"):
        database.final_degistirme()
    elif(islem=="6"):
        database.proje_degistirme()

    elif(islem=="q" or islem=="Q"):
        print("Sistemden Çıkış Yapılıyor...")
        time.sleep(2)
        break










