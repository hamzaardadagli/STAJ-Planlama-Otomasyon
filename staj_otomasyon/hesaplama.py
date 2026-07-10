import pandas as pd
import matplotlib.pyplot as plt

def verileri_isle(dosya_yolu):
    try:
        
        df = pd.read_excel(dosya_yolu)
        
        
        STOK_BAKIR = 5000  
        STOK_PVC = 10000  
        
        gerekli_bakir_listesi = []
        gerekli_pvc_listesi = []
        vardiya_sure_listesi = []
        stok_durum_listesi = []
        
        toplam_bakir_ihtiyaci = 0
        toplam_pvc_ihtiyaci = 0
        toplam_siparis_metresi = 0
        toplam_gerekli_vardiya = 0
        
        for index, row in df.iterrows():
            kablo_tipi = str(row["Kablo Tipi"]).strip().upper()
            metre = int(row["Siparis Metresi"])
            toplam_siparis_metresi += metre
            
            if "TTR" in kablo_tipi:
                satir_bakir = metre * 0.07
                satir_pvc = metre * 0.12
                satir_vardiya = round((metre / 6000) / 8, 2)
            elif "NYA" in kablo_tipi:
                satir_bakir = metre * 0.015
                satir_pvc = metre * 0.025
                satir_vardiya = round((metre / 12000) / 8, 2)
            else:
                satir_bakir = 0
                satir_pvc = 0
                satir_vardiya = 0
            
            toplam_bakir_ihtiyaci += satir_bakir
            toplam_pvc_ihtiyaci += satir_pvc
            toplam_gerekli_vardiya += satir_vardiya
            
            gerekli_bakir_listesi.append(round(satir_bakir, 2))
            gerekli_pvc_listesi.append(round(satir_pvc, 2))
            vardiya_sure_listesi.append(satir_vardiya)
            
            if satir_bakir <= STOK_BAKIR and satir_pvc <= STOK_PVC:
                stok_durum_listesi.append("STOK YETERLİ")
            else:
                stok_durum_listesi.append("STOK YETERSİZ / SATIN ALMA")

        df["Gerekli Bakir (Kg)"] = gerekli_bakir_listesi
        df["Gerekli PVC (Kg)"] = gerekli_pvc_listesi
        df["Gerekli Sure (Vardiya)"] = vardiya_sure_listesi
        df["Hammadde Stok Durumu"] = stok_durum_listesi
        
        eksik_bakir = max(0, toplam_bakir_ihtiyaci - STOK_BAKIR)
        eksik_pvc = max(0, toplam_pvc_ihtiyaci - STOK_PVC)
        satin_alma_uyarisi = "YOK (STOKLAR YETERLİ)" if (eksik_bakir == 0 and merge_pvc == 0) else "⚠️ ACİL HAMMADDE TEDARİKİ GEREKLİ!"
        
        
        df_mrp = pd.DataFrame({
            "Hammadde Adı": ["Bakır Filmaşin", "PVC Granül"],
            "Gerekli Miktar (Kg)": [round(toplam_bakir_ihtiyaci, 1), round(toplam_pvc_ihtiyaci, 1)],
            "Mevcut Stok (Kg)": [STOK_BAKIR, STOK_PVC],
            "Satın Alma İhtiyacı (Kg)": [round(eksik_bakir, 1), round(eksik_pvc, 1)]
        })
        
       
        cikti_dosyasi = "hesaplama_sonuclari.xlsx"
        with pd.ExcelWriter(cikti_dosyasi) as writer:
            
            df_mrp.to_excel(writer, sheet_name="Genel Hammadde MRP", index=False)
            df.to_excel(writer, sheet_name="Detayli Uretim Cizelgesi", index=False)
        
        
        ozet_metni = f"""
        <h3>⚡ KABLO ÜRETİM VE MALZEME PLANLAMA RAPORU</h3>
        <ul>
            <li><b>Toplam Alınan Kablo Siparişi:</b> {toplam_siparis_metresi:,} Metre</li>
            <li><b>⏱️ Ekstrüzyon / Büküm Hatları Toplam Süre İhtiyacı:</b> {toplam_gerekli_vardiya:.1f} Vardiya (8 Saatlik)</li>
            <li><b>Eksik Hammadde ve Satın Alma Durumu:</b> <span style='color: {"green" if "YOK" in satin_alma_uyarisi else "red"}'><b>{satin_alma_uyarisi}</b></span></li>
        </ul>
        <table border='1' cellpadding='5' style='border-collapse:collapse; text-align:center;'>
            <tr style='background-color:#d9e2ec;'>
                <th>Hammadde Adı</th>
                <th>Gerekli Miktar (Kg)</th>
                <th>Mevcut Stok (Kg)</th>
                <th>Satın Alma İhtiyacı (Kg)</th>
            </tr>
            <tr><td>Bakır Filmaşin</td><td>{toplam_bakir_ihtiyaci:,.1f}</td><td>{STOK_BAKIR:,}</td><td style='color: {"red" if eksik_bakir > 0 else "black"}'>{eksik_bakir:,.1f}</td></tr>
            <tr><td>PVC Granül</td><td>{toplam_pvc_ihtiyaci:,.1f}</td><td>{STOK_PVC:,}</td><td style='color: {"red" if eksik_pvc > 0 else "black"}'>{eksik_pvc:,.1f}</td></tr>
        </table>
        """
        
        
        plt.figure(figsize=(7, 5))
        hammaddeler = ["Bakir Filmasin", "PVC Granul"]
        miktarlar = [toplam_bakir_ihtiyaci, toplam_pvc_ihtiyaci]
        plt.bar(hammaddeler, miktarlar, color=['#b87333', '#4a5568'], edgecolor='black', width=0.5)
        plt.title("Üretim İçin Gerekli Hammadde Miktarları (Kg)", fontsize=12, fontweight='bold')
        plt.ylabel("Ağırlık (Kg)", fontsize=10)
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        for i, v in enumerate(miktarlar):
            plt.text(i, v + (max(miktarlar)*0.01), f"{v:,.1f} kg", ha='center', fontweight='bold')
        plt.savefig("kazanc_grafigi.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return ozet_metni
        
    except Exception as e:
        print(f"[HATA] Detaylı planlama analizi yapılırken hata: {e}")
        return None