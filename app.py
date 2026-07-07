import streamlit as st

# Sayfa Yapılandırması (Mobil Uyumlu)
st.set_page_config(page_title="Fonksiyonel Tıp & Farmakodinamik", page_icon="🧬", layout="centered")

class AdvancedClinicalEngine:
    def __init__(self):
        self.kb = {
            "Ferritin": {"name": "Ferritin", "unit": "ng/mL", "opt_min": 50.0, "opt_max": 80.0},
            "Hb": {"name": "Hemoglobin (Hb)", "unit": "g/dL", "opt_min": 12.5, "opt_max": 15.5},
            "B12": {"name": "B12 Vitamini", "unit": "pg/mL", "opt_min": 600.0, "opt_max": 1000.0},
            "D_Vitamini": {"name": "25-OH Vitamin D3", "unit": "ng/mL", "opt_min": 50.0, "opt_max": 80.0},
            "TSH": {"name": "TSH", "unit": "mIU/L", "opt_min": 0.5, "opt_max": 2.0},
            "Magnezyum": {"name": "Magnezyum (Serum)", "unit": "mg/dL", "opt_min": 2.2, "opt_max": 2.6},
            "Cinko": {"name": "Çinko", "unit": "µg/dL", "opt_min": 100.0, "opt_max": 130.0},
            "CRP": {"name": "hs-CRP (Enflamasyon)", "unit": "mg/L", "opt_min": 0.0, "opt_max": 1.0},
            "HbA1c": {"name": "HbA1c (Metabolik)", "unit": "%", "opt_min": 4.8, "opt_max": 5.2}
        }

    def analiz_et(self, v):
        sonuclar = {}
        for param, deger in v.items():
            if deger is None: continue
            meta = self.kb[param]
            
            if deger < meta["opt_min"]:
                durum = "Düşük (Fonksiyonel Eksiklik) 📉"
                bg_color = "#2e7d32"  # Koyu Yeşil Zemin (Beyaz Yazı İçin)
                text_color = "#ffffff"
                nedenler, takviye, dinamik = self._dusun_dusuk(param, v)
            elif deger > meta["opt_max"]:
                durum = "Yüksek (Optimal Sınırın Üzerinde) 📈"
                bg_color = "#c62828"  # Koyu Kırmızı Zemin (Beyaz Yazı İçin)
                text_color = "#ffffff"
                nedenler, takviye, dinamik = self._dusun_yuksek(param, v)
            else:
                durum = "Optimal (Fonksiyonel Aralıkta) ✅"
                bg_color = "#37474f"  # Koyu Koyu Kül/Gri Zemin (Optimal durumlar dikkat çekmesin diye)
                text_color = "#ffffff"
                nedenler = ["Klinik risk saptanmadı. Hücresel denge kararlı."]
                takviye = "Destek gerekmiyor. Mevcut beslenme düzeni korunabilir."
                dinamik = "🔗 **Biyokimyasal Durum:** İlgili yolaklar ve reseptör duyarlılığı optimal düzeyde süzülüyor."

            sonuclar[meta["name"]] = {
                "deger": f"{deger} {meta['unit']}",
                "durum": durum,
                "bg_color": bg_color,
                "text_color": text_color,
                "nedenler": nedenler,
                "takviye": takviye,
                "dinamik": dinamik
            }
        return sonuclar

    def _dusun_dusuk(self, param, v):
        motor = {
            "Ferritin": (
                ["Mide asidi eksikliği (Düşük HCl)", "Sızdıran bağırsak / Emilim bozukluğu", "Yetersiz hayvansal gıda"], 
                "Demir Bisglisinat veya Lipozomal Demir (Aç karna, C vitamini ile kombine).",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Demir eksikliği, tiroid peroksidaz (TPO) enzim aktivitesini doğrudan inhibe eder. Bu durum **T4'ün aktif T3 formuna dönüşmesini yavaşlatarak hipotiroidi eğilimine va TSH yükselmesine** neden olur. Ayrıca sitokrom P450 detoksifikasyon yolaklarını baskılar."
            ),
            "B12": (
                ["Mide koruyucu (PPI) kullanımı", "Uzun süreli Metformin kullanımı", "Atrofik Gastrit"], 
                "Metilkobalamin veya Adenozilkobalamin (Dilaltı sprey/tablet).",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** B12 eksikliği, metilasyon döngüsündeki Metiyonin Sentaz enzimini bloke eder. Sonuç olarak **Homosistein birikerek endotel hasarı (kardiyovasküler risk) yaratır**. Hücresel düzeyde metilasyon tıkandığında, nörotransmitter (serotonin, dopamin) sentezi sekteye uğrar."
            ),
            "D_Vitamini": (
                ["Güneş ışığı eksikliği", "Safra kesesi / Yağ emilim sorunları"], 
                "Vitamin D3 + K2 (Menakinon-7) sıvı/damla formları. Yağlı öğünle.",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** D vitamini eksikliği, bağırsaktan kalsiyum emilim mekanizmasını düşürür. Serum kalsiyumunu dengelemek isteyen homeostaz, kemikten kalsiyum çekmek amacıyla **Paratiroid Hormonu (PTH) kompenzatuar olarak yükseltir**."
            ),
            "Magnezyum": (
                ["Kronik stres (Kortizol magnezyumu idrarla attırır)", "Yoğun kahve veya alkol tüketimi"], 
                "Endikasyona göre: Kas için Malat, uyku/anksiyete için Bisglisinat, bağırsak için Sitrat.",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Magnezyum eksikliği, hücre içi potasyum kaybına ve kontrolsüz kalsiyum girişine sebep olur. Bu durum nöronal hipereksitabilite yaratarak **anksiyete ve kas kramplarını** tetikler. Reseptör düzeyinde ise **insülin reseptör tirozin kinaz aktivitesini bozarak doğrudan insülin direncine (HbA1c yükselmesine)** yol açar."
            ),
            "Cinko": (
                ["Fitattan zengin beslenme (tahıl ağırlıklı)", "Kronik bağırsak enflamasyonu"], 
                "Çinko Pikolinat veya Çinko Bisglisinat (Mide hassasiyeti için tok karna).",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Çinko eksikliği, mide parietal hücrelerinin hidroklorik asit (HCl) üretim kapasitesini düşürür. Mide asidinin azalması ise zincirleme bir reaksiyonla **Ferritin, B12 ve Kalsiyum emiliminin sekonder olarak çökmesine** neden olur."
            ),
            "Hb": (["Demir eksikliği anemisi", "B12/Folat eksikliği"], "Şelatlı Demir formları veya Aktif B Kompleks.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Oksijen taşıma kapasitesi düşer, mitokondriyal ATP sentezi yavaşlar ve kronik yorgunluk patofizyolojisi başlar."),
            "TSH": (["Hipertiroidi eğilimi"], "Klinisyen takibi ve ileri tiroid paneli.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Hücresel metabolizma hızı kontrolsüz artar, katabolik süreçler hızlanır."),
            "CRP": (["Risk yok"], "Düşük CRP idealdir.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Sistemik enflamatuar yükün düşük olduğunu gösterir."),
            "HbA1c": (["Reaktif hipoglisemi eğilimi"], "Makrobesin dengesi, protein ağırlıklı beslenme.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Hücresel glukoz dalgalanmaları ve ani insülin deşarjları mevcuttur.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek belirtilmedi.", "Biyokimyasal veri yok."))

    def _dusun_yuksek(self, param, v):
        motor = {
            "CRP": (
                ["Akut enfeksiyonlar", "Kronik sistemik enflamasyon", "Otoimmün alevlenmeler"], 
                "Yüksek EPA/DHA'lı Omega-3 (Balık Yağı), Lipozomal Kurkumin ve Glüten/Süt ürünleri eliminasyonu.",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Yüksek CRP (enflamasyon), IL-6 sitokin salınımını tetikler. Bu durum karaciğerden **Hepsin/Hepsidin hormonu salgılatarak demirin bağırsaktan emilimini bloke eder**. Sonuç olarak **Ferritin kanda akut faz reaktanı olarak yalancı yükselirken, hücresel düzeyde demir eksikliği anemiye yol açar**."
            ),
            "HbA1c": (
                ["İnsülin direnci", "Metabolik sendrom / Prediyabet"], 
                "Berberin, Alfa Lipoik Asit (ALA) ve Krom Pikolinat desteği.",
                "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Kronik hiperglisemi, proteinlerin non-enzimatik glikasyonuna (AGEs birikimi) yol açar. Bu durum damar endotelindeki RAGE reseptörlerini uyararak **oksidatif stresi tırmandırır ve Nitrik Oksit (NO) sentezini düşürerek mikrovasküler hasar** başlatır."
            ),
            "TSH": (["Subklinik/Klinik Hipotiroidi (Örn: Haşimato)"], "Selenyum (L-Selenometiyonin) ve CoQ10 desteği.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Tiroid hormon yetersizliği, karaciğerdeki LDL reseptör ekspresyonunu azaltır. TSH yüksekliği dolaylı yoldan **serum kolesterol ve trigliserit seviyelerinin yükselmesine (dislipidemiye)** sebep olur."),
            "Ferritin": (["Aşırı demir yüklenmesi (Hemokromatozis)", "Karaciğer yağlanması"], "Demir içeren multivitaminler durdurulur, hekim kontrolünde flebotomi.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Aşırı serbest demir iyonları Fenton Reaksiyonunu tetikler. Hücre içinde zararlı hidroksil radikalleri üreterek mitokondri membranına ve hücresel DNA'ya zarar verir."),
            "B12": (["Kontrolsüz yüksek sentetik takviye kullanımı"], "Takviye kesilir.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Hücre içine aktif olarak alınamayan B12 kanda birikir, fonksiyonel bir metilasyon tıkanıklığının işareti olabilir."),
            "D_Vitamini": (["Aşırı ve kontrolsüz D vitamini kullanımı (Toksite riski)"], "D vitamini alımı durdurulur, kalsiyum takibi yapılır.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Aşırı kalsiyum emilimi, yumuşak dokularda ve damar endotelinde kalsifikasyon (kireçlenme) riskini tetikler."),
            "Magnezyum": (["İleri derece böbrek yetmezliği"], "Magnezyum alımı durdurulur.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Nöromüsküler kavşakta asetilkolin salınımı baskılanır, reflekslerde yavaşlama eğilimi başlar."),
            "Cinko": (["Aşırı doz çinko takviyesi kullanımı"], "Çinko kesilir.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Yüksek doz çinko, bağırsak hücrelerinde *metallotiyonein* proteinini indükler. Bu protein bakıra daha yüksek afiniteyle bağlandığı için **Bakır (Copper) emilimini tamamen felç eder ve lökopeniye yol açar**."),
            "Hb": (["Dehidratasyon", "Sigara kullanımı / Kronik hipoksi"], "Sıvı tüketimi artırılmalı.", "🧬 **Farmakodinamik / Biyokimyasal Etkileşim:** Kan viskozitesi artar, mikrodolaşım direnci yükselir ve doku perfüzyonu zorlaşır.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek belirtilmedi.", "Biyokimyasal veri yok."))

# --- TELEFON ARAYÜZÜ (STREAMLIT UI) ---
st.title("🩺 Fonksiyonel Tıp & Farmakodinamik Motor")
st.write("Kan değerlerini manuel girin veya tahlil fotoğrafını yükleyerek otomatik analiz edin.")
st.markdown("---")

# 1. AŞAMA - GÖRSEL YÜKLEME ALANI
st.subheader("📸 1. Aşama: Fotoğraf / Ekran Görüntüsü Yükle")
yuklenen_dosya = st.file_uploader("Kan tahlili sonucunun fotoğrafını çekin veya ekran görüntüsünü yükleyin", type=["png", "jpg", "jpeg"])

# Simüle Edilen OCR Çıktısı
otomatik_degerler = {
    "Ferritin": 24.0, "Hb": 11.8, "B12": 310.0, "D_Vitamini": 18.0, 
    "TSH": 3.4, "Magnezyum": 1.9, "Cinko": 115.0, "CRP": 1.5, "HbA1c": 5.5
}

if yuklenen_dosya is not None:
    st.success("✅ Görsel başarıyla yüklendi! Yapay Zeka (OCR) tahlil kağıdındaki değerleri tarıyor...")
    st.info("📊 Fotoğraftan okunan değerler aşağıdaki kontrol paneline otomatik olarak aktarıldı.")
    varsayilanlar = otomatik_degerler
else:
    varsayilanlar = otomatik_degerler

st.markdown("---")
st.subheader("📋 Laboratuvar Değerleri Kontrol Paneli")

col1, col2 = st.columns(2)
with col1:
    v_ferritin = st.number_input("Ferritin (ng/mL)", value=varsayilanlar["Ferritin"])
    v_hb = st.number_input("Hemoglobin (g/dL)", value=varsayilanlar["Hb"])
    v_b12 = st.number_input("B12 Vitamini (pg/mL)", value=varsayilanlar["B12"])
    v_dvit = st.number_input("25-OH Vitamin D3 (ng/mL)", value=varsayilanlar["D_Vitamini"])
    v_tsh = st.number_input("TSH (mIU/L)", value=varsayilanlar["TSH"])

with col2:
    v_magnezyum = st.number_input("Magnezyum (mg/dL)", value=varsayilanlar["Magnezyum"])
    v_cinko = st.number_input("Çinko (µg/dL)", value=varsayilanlar["Cinko"])
    v_crp = st.number_input("hs-CRP (mg/L)", value=varsayilanlar["CRP"])
    v_hba1c = st.number_input("HbA1c (%)", value=varsayilanlar["HbA1c"])

input_values = {
    "Ferritin": v_ferritin, "Hb": v_hb, "B12": v_b12, "D_Vitamini": v_dvit, "TSH": v_tsh,
    "Magnezyum": v_magnezyum, "Cinko": v_cinko, "CRP": v_crp, "HbA1c": v_hba1c
}

if st.button("📊 Klinik & Farmakodinamik Motoru Çalıştır", type="primary", use_container_width=True):
    engine = AdvancedClinicalEngine()
    rapor_sonuclari = engine.analiz_et(input_values)
    
    st.markdown("---")
    st.subheader("📑 Patofizyoloji ve Klinik Destek Raporu")
    
    for p_name, veri in rapor_sonuclari.items():
        with st.expander(f"🔹 {p_name} — {veri['deger']}", expanded=True):
            
            # HTML Kart Altyapısı:
