import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

# Tkinter Arayüzü
root = tk.Tk()
root.title("Hava Durumu Otomasyonu")
root.geometry("400x300")

log_text = tk.Text(root, height=15, width=45)
log_text.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack()

def log_yaz(mesaj):
    def guncelle():
        log_text.insert(tk.END, mesaj + "\n")
        log_text.see(tk.END)
        print(mesaj)
    log_text.after(0, guncelle)  # Ana thread üzerinden güncelleme yapıyoruz

# ---------- Selenium Fonksiyonları ----------

def kontrol_baslik(driver):
    log_yaz(f"Sayfa Başlığı: {driver.title}")

def ekran_goruntusu_al(driver, sehir):
    dosya_adi = f"{sehir}_hava_durumu.png"
    driver.save_screenshot(dosya_adi)
    log_yaz(f"Ekran görüntüsü kaydedildi: {dosya_adi}")

def javascript_ornegi(driver):
    log_yaz("JavaScript ile arka plan rengi değiştiriliyor...")
    driver.execute_script("document.body.style.backgroundColor = '#FAFAD2';")

def sayfa_kaydir(driver):
    log_yaz("Sayfa aşağı kaydırılıyor...")
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

def yeni_sekmede_sorgu(driver, yeni_sehir):
    log_yaz(f"Yeni sekmede '{yeni_sehir}' için arama yapılıyor...")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://www.google.com")
    time.sleep(1)
    arama = driver.find_element(By.NAME, "q")
    arama.send_keys(f"{yeni_sehir} hava durumu")
    arama.send_keys(Keys.ENTER)
    time.sleep(3)
    derece = driver.find_element(By.ID, "wob_tm").text
    durum = driver.find_element(By.ID, "wob_dc").text
    log_yaz(f"{yeni_sehir} için hava: {derece}°C, {durum}")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Ekstra Fonksiyonlar:
def sayfa_yuklenmesini_bekle(driver):
    log_yaz("Sayfa tamamen yüklenene kadar bekleniyor...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "wob_tm"))
    )
    log_yaz("Sayfa yüklendi!")

def butona_tikla(driver):
    log_yaz("Butona tıklanıyor...")
    buton = driver.find_element(By.ID, "some_button_id")  # Bu örnek ID ile buton buluyor
    buton.click()
    log_yaz("Butona tıklanmış oldu.")

def formu_gonder(driver):
    log_yaz("Form dolduruluyor...")
    input_box = driver.find_element(By.ID, "input_field_id")
    input_box.send_keys("Test Verisi")
    submit_button = driver.find_element(By.ID, "submit_button_id")
    submit_button.click()
    log_yaz("Form gönderildi.")

def sayfa_bilgileri_al(driver):
    baslik = driver.title
    url = driver.current_url
    log_yaz(f"Sayfa Başlığı: {baslik}")
    log_yaz(f"Sayfa URL: {url}")

def tarayici_minimize_et(driver):
    log_yaz("Tarayıcı minimize ediliyor...")
    driver.minimize_window()

def drag_and_drop(driver):
    log_yaz("Sürükle ve bırak işlemi başlatılıyor...")
    source_element = driver.find_element(By.ID, "img1")  # Kaynak öğe
    target_element = driver.find_element(By.ID, "div1")  # Hedef öğe
    actions = ActionChains(driver)
    actions.drag_and_drop(source_element, target_element).perform()
    log_yaz("Sürükle ve bırak işlemi tamamlandı.")

# ---------- Ana İşlem Fonksiyonu ----------

def selenium_islem(sehir):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    try:
        log_yaz("Chrome başlatılıyor...")
        driver = webdriver.Chrome(options=options)

        log_yaz("Google'a gidiliyor...")
        driver.get("https://www.google.com")
        time.sleep(2)

        kontrol_baslik(driver)

        log_yaz("Arama kutusu bulunuyor...")
        arama = driver.find_element(By.NAME, "q")
        arama.send_keys(f"{sehir} hava durumu")
        arama.send_keys(Keys.ENTER)

        sayfa_yuklenmesini_bekle(driver)

        time.sleep(3)
        log_yaz("Hava durumu bilgisi alınıyor...")
        derece = driver.find_element(By.ID, "wob_tm").text
        durum = driver.find_element(By.ID, "wob_dc").text

        sonuc = f"{sehir} için hava: {derece}°C, {durum}"
        log_yaz("✅ " + sonuc)
        messagebox.showinfo("Sonuç", sonuc)

        ekran_goruntusu_al(driver, sehir)
        javascript_ornegi(driver)
        sayfa_kaydir(driver)
        yeni_sekmede_sorgu(driver, "İzmir")
        
        # Ekstra fonksiyonlar
        sayfa_bilgileri_al(driver)
        tarayici_minimize_et(driver)

    except Exception as e:
        log_yaz(f"❌ Hata oluştu: {e}")
    finally:
        time.sleep(2)

        log_yaz("Tarayıcı kapatıldı.")

# ---------- Tkinter Button Fonksiyonu ----------

def baslat():
    sehir = entry.get().strip()
    if not sehir:
        messagebox.showwarning("Uyarı", "Lütfen bir şehir adı girin.")
        return

    log_text.delete(1.0, tk.END)  # önceki logları temizle
    log_yaz(f"'{sehir}' için işlem başlatılıyor...")

    t = threading.Thread(target=selenium_islem, args=(sehir,))
    t.start()

def baslat_surukle():
    
  
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")  # type: ignore # SSL hatalarını yoksay
    options.add_argument("--start-maximized") # type: ignore
    driver = webdriver.Chrome(options=options)  # SSL hataları yoksayarak başlatıyoruz

    try:
        
        log_yaz("W3Schools sayfasına gidiliyor...")
        driver.get("https://www.w3schools.com/html/html5_draganddrop.asp")
        time.sleep(2)

        # 5 defa sürükle-bırak işlemi
        for i in range(1):
            try:
                # Sürüklenebilir öğe (img)
                source_element = driver.find_element(By.ID, "img1")

                # Hedef alan (div1)
                target_element = driver.find_element(By.ID, "div2")

                # ActionChains kullanarak sürükle ve bırak işlemi
                actions = ActionChains(driver)
                actions.drag_and_drop(source_element, target_element).perform()

                # Her işlem sonrası 1 saniye bekle
                time.sleep(1)

                log_yaz(f"{i+1}. işlem tamamlandı.")
            except Exception as e:
                log_yaz(f"❌ Hata oluştu: {e}")
                break

        log_yaz("Sürükle ve bırak işlemi tamamlandı.")
        time.sleep(3)
    except Exception as e:
        log_yaz(f"❌ Hata oluştu: {e}")
    finally:
        driver.quit()

def sekmeler_arasi_gecis():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        log_yaz("🔍 İlk sekme açılıyor: Google")
        driver.get("https://www.google.com")

        log_yaz("🆕 Yeni sekme açılıyor: W3Schools")
        driver.execute_script("window.open('https://www.w3schools.com');")

        tabs = driver.window_handles  # tüm sekmeleri al

        for i in range(3):
            log_yaz(f"🔁 {i+1}. geçiş: Sekme 1'e geçiliyor...")
            driver.switch_to.window(tabs[0])
            time.sleep(3)

            log_yaz(f"🔁 {i+1}. geçiş: Sekme 2'ye geçiliyor...")
            driver.switch_to.window(tabs[1])
            time.sleep(3)

        log_yaz("✅ Sekmeler arası geçiş tamamlandı.")

    except Exception as e:
        log_yaz(f"❌ Hata oluştu: {e}")
    finally:
        driver.quit()

# ---------- Tkinter Arayüz Elemanları ----------

button = tk.Button(root, text="Hava Durumu Sorgula", command=baslat)
button.pack(pady=5)

# Drag and Drop işlemi için buton ekliyoruz
button2 = tk.Button(root, text="Sürükle ve Bırak Testi", command=baslat_surukle)
button2.pack(pady=10)
button3 = tk.Button(root, text="Sekmeler Arası Geçiş", command=sekmeler_arasi_gecis)
button3.pack(pady=15)


# ---------- Başlat ----------
root.mainloop()
