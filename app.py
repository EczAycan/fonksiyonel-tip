import streamlit as st
from datetime import datetime

# Sayfa Yapılandırması (Mobil Uyumlu)
st.set_page_config(page_title="Fonksiyonel Tıp Pro", page_icon="🩺", layout="centered")

class AdvancedClinicalEngine:
    def __init__(self):
        # Aşama 1 & Aşama 3 Hazırlık: Temel Bilgi Bankası
        self.kb = {
            "Ferritin": {"name": "Ferritin", "unit": "ng/mL", "opt_min": 50.0, "opt_max": 80.0},
            "Hb": {"name": "Hemoglobin (Hb)", "unit": "g/dL", "opt_min": 12.5, "opt_max": 15.5},
            "B12": {"name": "B12 Vitamini", "unit": "pg/mL", "opt_min": 600.0, "opt_max": 1000.0},
            "D_Vitamini": {"name": "25-OH Vitamin D3", "unit": "ng/mL", "opt_min": 50.0, "opt_max": 80.0},
            "TSH": {"name": "TSH", "unit": "mIU/L", "opt_min": 0.5, "opt_max": 2.0},
            "Magnezyum": {"name": "Magnezyum (Serum)", "unit": "mg/dL", "opt_min": 2.2, "opt_max": 2.6},
            "Cinko": {"name": "Çinko", "unit": "µg/dL", "opt_min": 100.0, "opt_max": 130.0},
            "CRP": {"name": "hs-CRP (Enflamasyon)", "unit": "mg/L", "opt_min": 0.0, "opt_max": 1.0},
            "HbA1c": {"name": "HbA1c (Metabolik)", "unit": "%", "opt_min": 4.8, "opt_max": 5.2},
            # Aşama 2 İçin Eklenen Organ Fonksiyon Parametreleri
            "ALT": {"name": "ALT (Karaciğer)", "unit": "U/L", "normal_max": 45.0},
            "Kreatinin": {"name": "Kreatinin (Böbrek)", "unit": "mg/dL", "normal_max": 1.2}
        }

    def analiz_et(self, v, info):
        sonuclar = {}
        
        # Aşama 2: Dinamik Filtreler (Cinsiyet ve Gebelik Ayarlamaları)
        if info["gebelik"]:
            self.kb["TSH"]["opt_max"] = 2.5  # Gebelikte TSH üst sınırı fonksiyonel olarak daha kısıtlıdır
            self.kb["Ferritin"]["opt_min"] = 40.0 # Gebelikte hemodilüsyondan dolayı esnetilebilir
        elif info["cinsiyet"] == "Erkek":
            self.kb["Ferritin"]["opt_min"] = 70.0
            self.kb["Ferritin"]["opt_max"] = 120.0
            self.kb["Hb"]["opt_min"] = 13.5
            self.kb["Hb"]["opt_max"] = 17.5

        # Karaciğer ve Böbrek Hasar Kontrolü (Aşama 2 Süzgeci)
        karaciger_hasari = v.get("ALT", 0) > self.kb["ALT"]["normal_max"]
        bobrek_yetmezligi = v.get("Kreatinin", 0) > self.kb["Kreatinin"]["normal_max"]

        for param, deger in v.items():
            if deger is None or param in ["ALT", "Kreatinin"]: continue
            meta = self.kb[param]
            
            # 2. AŞAMA: OTOMATİK YORUM
            if deger < meta["opt_min"]:
                durum = "Düşük (Fonksiyonel Eksiklik) 📉"
                # 3. AŞAMA: OLASI NEDENLER & 4. AŞAMA: TAKVİYE ÖNERİSİ
                nedenler, takviye = self._dusun_dusuk(param, v)
            elif deger > meta["opt_max"]:
                durum = "Yüksek (Optimal Sınırın Üzerinde) 📈"
                nedenler, takviye = self._dusun_yuksek(param, v)
            else:
                durum = "Optimal (Fonksiyonel Aralıkta) ✅"
                nedenler = ["Klinik risk saptanmadı. Hücresel denge kararlı."]
                takviye = "Destek gerekmiyor. Mevcut beslenme düzeni korunabilir."

            # Aşama 2: İlaç ve Organ Uyarı Karar Mekanizması (Güvenlik Süzgeci)
            if "Düşük" in durum:
                if param == "Magnezyum" and bobrek_yetmezligi:
                    takviye = "⚠️ UYARI: Böbrek fonksiyonları (Kreatinin) yüksek! Hekim onayı olmadan Magnezyum takviyesi verilmemelidir (Hipermagnezemi riski)."
                if param == "Cinko" and karaciger_hasari:
                    takviye = "⚠️ UYARI: Karaciğer enzimleri yüksek. Çinko desteği verilirken yüksek dozlardan kaçınılmalı, emilim kontrol edilmelidir."

            sonuclar[meta["name"]] = {
                "deger": f"{deger} {meta['unit']}",
                "durum": durum,
                "nedenler": nedenler,
                "takviye": takviye
            }
        return sonuclar

    def _dusun_dusuk(self, param, v):
        # Klinik Bilgi Motoru - Düşük Değerler
        motor = {
            "Ferritin": (["Yetersiz hayvansal gıda", "Mide asidi eksikliği", "Sızdıran bağırsak/emilim bozukluğu", "Aşırı menstrüel kanama"], "Demir Bisglisinat veya Lipozomal Demir (Aç karna, C vitamini ile)."),
            "Hb": (["Demir eksikliği anemisi", "B12/Folat eksikliği (Makrositer)", "Kronik hastalık yükü"], "Anemi türüne göre Aktif B Kompleks (Metilfolat) veya şelatlı Demir formları."),
            "B12": (["Vegan/Vejetaryen beslenme", "Mide koruyucu (PPI) kullanımı", "Metformin kullanımı", "Atrofik Gastrit"], "Metilkobalamin veya Adenozilkobalamin (Dilaltı sprey/tablet)."),
            "D_Vitamini": (["Güneş ışığı eksikliği", "Safra kesesi/yağ emilim sorunları", "Obezite"], "Vitamin D3 + K2 (Menakinon-7) sıvı/damla formları. Yağlı öğünle."),
            "TSH": (["Hipertiroidi eğilimi", "Aşırı doz tiroid ilacı kullanımı"], "Klinisyen takibi, ileri tiroid paneli (sT3, sT4) ve antikor testi gerekir."),
            "Magnezyum": (["Yetersiz yeşil yapraklı sebze tüketimi", "Kronik stres (Magnezyum tüketir)", "Alkol veya yoğun kahve tüketimi"], "Klinik duruma göre: Kas için Malat, uyku/anksiyete için Bisglisinat, bağırsak için Sitrat."),
            "Cinko": (["Fitangillerden zengin beslenme (tahıl ağırlıklı)", "Kronik bağırsak enflamasyonu"], "Çinko Pikolinat veya Çinko Bisglisinat (Mide hassasiyetini önlemek için tok karna)."),
            "CRP": (["Risk yok"], "Düşük CRP idealdir."),
            "HbA1c": (["Reaktif hipoglisemi eğilimi", "Uzun süreli aşırı düşük kalori alımı"], "Karbonhidrat kalitesi artırılmalı, öğün protein dengesi sağlanmalı.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek belirtilmedi."))

    def _dusun_yuksek(self, param, v):
        # Klinik Bilgi Motoru - Yüksek Değerler
        if param == "Ferritin" and v.get("CRP", 0) > 1.0:
            return (["Sistemik kronik enflamasyona bağlı Akut Faz Yanıtı (Yalancı yükseklik)"], "Demir verilmez! Enflamasyonu çözmek için Yüksek EPA/DHA'lı Omega-3 ve Lipozomal Kurkumin planlanır.")
        
        motor = {
            "Ferritin": (["Aşırı demir yüklenmesi (Hemokromatozis)", "Karaciğer yağlanması (Metabolik sendrom)"], "Demir içeren multivitaminler durdurulur. Hekim kontrolünde kan bağışı / flebotomi."),
            "Hb": (["Dehidratasyon (Vücudun susuz kalması)", "Sigara kullanımı / Hipoksi"], "Günlük su tüketimi artırılmalı, hipoksik faktörler elenmeli."),
            "B12": (["Kontrolsüz yüksek sentetik takviye kullanımı", "Metilasyon döngüsü tıkanıklığı"], "Takviye kesilir. Hücresel fonksiyonu görmek için Homosistein bakılmalıdır."),
            "D_Vitamini": (["Aşırı ve kontrolsüz D vitamini kullanımı (Toksite riski)"], "D vitamini alımı durdurulur, serum kalsiyum takibi yapılır."),
            "TSH": (["Subklinik/Klinik Hipotiroidi (Örn: Haşimato)", "Selenyum ve Çinko eksikliği", "Aşırı florür/klorür maruziyeti"], "T4 -> T3 dönüşüm desteği: Selenyum (L-Selenometiyonin), Çinko Bisglisinat ve Magnezyum."),
            "Magnezyum": (["İleri derece böbrek yetmezliği", "Aşırı doz magnezyum infüzyonu"], "Magnezyum alımı durdurulur. Renal fonksiyonlar incelenir."),
            "Cinko": (["Aşırı doz çinko takviyesi kullanımı"], "Çinko kesilir. Uzun süre yüksek kaldıysa Bakır (Copper) eksikliği yönünden incelenir."),
            "CRP": (["Akut enfeksiyon", "Kronik sistemik enflamasyon", "Otoimmün alevlenme"], "Yüksek doz Omega-3 (Balık Yağı), Kurkumin, Resveratrol ve Glüten/Süt ürünleri eliminasyon diyeti."),
            "HbA1c": (["İnsülin direnci", "Prediyabet / Diyabet", "Gelişmiş Glikasyon Ürünleri (AGEs) yüksekliği"], "Berberin, Alfa Lipoik Asit (ALA) ve Krom Pikolinat. Karbonhidrat kısıtlaması.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek belirtilmedi."))

# --- TELEFON ARAYÜZÜ (STREAMLIT UI) ---
st.title("🩺 Fonksiyonel Tıp - Klinik Motor")
st.write("Hasta parametrelerini girerek 4 aşamalı uzman analiz raporunu simüle edin.")
st.markdown("---")

# AŞAMA 2: HASTA FİLTRELERİ (Sidebar / Yan Menü)
st.sidebar.header("👤 Hasta Demografisi & Filtreler")
yas = st.sidebar.number_input("Yaş", min_value=0, max_value=120, value=35)
cinsiyet = st.sidebar.selectbox("Cinsiyet", ["Kadın", "Erkek"])

gebelik = False
if cinsiyet == "Kadın":
    gebelik = st.sidebar.checkbox("🤰 Gebelik Modu Aktif")

st.sidebar.markdown("---")
st.sidebar.header("🧪 Organ Fonksiyonları (Aşama 2)")
alt = st.sidebar.number_input("ALT (Karaciğer Enzimi) - U/L", min_value=0.0, value=25.0)
kreatinin = st.sidebar.number_input("Kreatinin (Böbrek) - mg/dL", min_value=0.0, value=0.8, step=0.1)

# AŞAMA 1: LABORATUVAR PARAMETRELERİ GİRİŞİ
st.subheader("📋 1. Aşama: Kan Değerleri Girişi")

col1, col2 = st.columns(2)
with col1:
    v_ferritin = st.number_input("Ferritin (ng/mL)", value=24.0)
    v_hb = st.number_input("Hemoglobin (g/dL)", value=11.8)
    v_b12 = st.number_input("B12 Vitamini (pg/mL)", value=310.0)
    v_dvit = st.number_input("25-OH Vitamin D3 (ng/mL)", value=18.0)
    v_tsh = st.number_input("TSH (mIU/L)", value=3.4)

with col2:
    v_magnezyum = st.number_input("Magnezyum (mg/dL)", value=1.9)
    v_cinko = st.number_input("Çinko (µg/dL)", value=115.0)
    v_crp = st.number_input("hs-CRP (mg/L)", value=0.4)
    v_hba1c = st.number_input("HbA1c (%)", value=5.5)

input_values = {
    "Ferritin": v_ferritin, "Hb": v_hb, "B12": v_b12, "D_Vitamini": v_dvit, "TSH": v_tsh,
    "Magnezyum": v_magnezyum, "Cinko": v_cinko, "CRP": v_crp, "HbA1c": v_hba1c,
    "ALT": alt, "Kreatinin": kreatinin
}
patient_info = {"yas": yas, "cinsiyet": cinsiyet, "gebelik": gebelik}

# ANALİZ BUTONU VE RAPORLAMA (Aşama 3 İpuçları İçerir)
if st.button("📊 Klinik Motoru Çalıştır", type="primary", use_container_width=True):
    engine = AdvancedClinicalEngine()
    rapor_sonuclari = engine.analiz_et(input_values, patient_info)
    
    st.markdown("---")
    st.subheader("📑 4 Aşamalı Bütüncül Analiz Çıktısı")
    
    for p_name, veri in rapor_sonuclari.items():
        with st.expander(f"🔹 {p_name} — {veri['deger']} ({veri['durum']})", expanded=True):
            
            # 2. Aşama: Durum Değerlendirmesi
            st.markdown(f"**[2. Aşama] Otomatik Yorum:** {veri['durum']}")
            
            # 3. Aşama: Olası Nedenler
            st.markdown("**[3. Aşama] Olası Klinik Nedenler:**")
            for n in veri['nedenler']:
                st.markdown(f"- {n}")
                
            # 4. Aşama: Takviye Önerisi
            st.markdown(f"💡 **[4. Aşama] OTC ve Destek Önerisi:**\n*{veri['takviye']}*")

    # Aşama 3 Pro Sürüm Altyapı Bildirimi (Mockup)
    st.info("ℹ️ **Aşama 3 Altyapı Notu:** PDF Rapor Çıktısı Modülü ve Bulut Yedekleme entegrasyonu için veritabanı bağlantısı dinlemededir.")
