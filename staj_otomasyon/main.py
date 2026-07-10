import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hesaplama
import mail_gonder


LOG_DOSYA_YOLU = r"C:\Users\HP\Desktop\staj_otomasyon\otomasyon_gunlugu.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DOSYA_YOLU, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


class KabloSiparisCasusu(FileSystemEventHandler):
    def on_created(self, event):
       
        if event.is_directory or not event.src_path.endswith('.xlsx') or "~$" in event.src_path:
            return
            
        dosya_adi = os.path.basename(event.src_path)
        logging.info(f"⚙️ [SİPARİŞ ALINDI] Klasöre yeni kablo sipariş listesi düştü: {dosya_adi}")
        
        
        time.sleep(2) 
        
        siparis_excel_yolu = event.src_path
        
        
        kablo_mrp_ozeti = hesaplama.verileri_isle(siparis_excel_yolu)
        
       
        mrp_excel_sonuc = "hesaplama_sonuclari.xlsx"
        hammadde_grafik_sonuc = "kazanc_grafigi.png"
        
      
        if kablo_mrp_ozeti and os.path.exists(mrp_excel_sonuc) and os.path.exists(hammadde_grafik_sonuc):
            logging.info("📊 [PLANLAMA TAMAMLANDI] Hammadde patlatma ve vardiya hesapları bitti. Mail gönderiliyor...")
            
            # Parametreleri gönderiyoruz
            mail_gonder.mail_gonder(mrp_excel_sonuc, hammadde_grafik_sonuc, kablo_mrp_ozeti, "hamzaardadagli07@gmail.com")
            
            logging.info(f"✅ [BAŞARILI] Kablo MRP Raporu ve grafik şeması fabrikaya postalandı.\n" + "="*60)
        else:
            logging.error(f"❌ [HATA] Sipariş işlenirken veya hammadde grafiği üretilirken bir sorun oluştu! Dosya: {dosya_adi}")


def kablo_botunu_baslat():
    izlenecek_klasor = "./gelen_kutusu"
    if not os.path.exists(izlenecek_klasor):
        os.makedirs(izlenecek_klasor)
        
    event_handler = KabloSiparisCasusu()
    observer = Observer()
    observer.schedule(event_handler, path=izlenecek_klasor, recursive=False)
    
    logging.info("⚡ === KABLO ÜRETİM PLANLAMA ARKA PLAN BOTU AKTİF ===")
    logging.info(f"📋 Gözler '{izlenecek_klasor}' klasöründe, yeni sipariş Excel'leri bekleniyor...")
    observer.start()
    
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        observer.stop()
        logging.info("🛑 Bot kullanıcı müdahalesiyle durduruldu.")
    observer.join()

if __name__ == "__main__":
    kablo_botunu_baslat()