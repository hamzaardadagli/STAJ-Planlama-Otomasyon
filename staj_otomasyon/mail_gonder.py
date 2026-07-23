import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def mail_gonder(excel_dosyasi, grafik_dosyasi, planlama_ozeti, alici_mail):
    gonderici = "hamzaardadagli07@gmail.com" 
    sifre = "agwu pocs aqne zmkm"          
    
    msg = MIMEMultipart()
    msg['From'] = gonderici
    msg['To'] = alici_mail
    msg['Subject'] = "⚡ KABLO FABRİKASI - Otomatik Hammadde Patlatma ve Hat Vardiya Planı"
    
    icerik = f"""
    <html>
      <body>
        <h2>Sayın Planlama Müdürü,</h2>
        <p>Sisteme yeni düşen kablo metraj sipariş verileri incelenmiş, ekstrüzyon hat hızlarına göre üretim süreleri ve hammadde tonaj ihtiyaçları hesaplanmıştır.</p>
        
        {planlama_ozeti}
        
        <p>Üretim hatları detaylı MRP Excel tablosu ve hammadde ağırlık grafik şeması ekte yer almaktadır.</p>
        <p><i>Bu otomasyon kablo üretim planlama birimi için özel olarak geliştirilmiştir.</i></p>
      </body>
    </html>
    """
    msg.attach(MIMEText(icerik, 'html'))
    
    dosyalar = [excel_dosyasi, grafik_dosyasi]
    try:
        for dosya_adi in dosyalar:
            with open(dosya_adi, "rb") as dosya:
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(dosya.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f"attachment; filename= {dosya_adi}")
                msg.attach(p)
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderici, sifre)
        server.sendmail(gonderici, alici_mail, msg.as_string())
        server.quit()
        print(f"[OK] Kablo Üretim Planlama Raporu gönderildi: {alici_mail}")
            
    except Exception as e:
        print(f"[HATA] Kablo planlama maili gönderilirken sorun çıktı: {e}")
