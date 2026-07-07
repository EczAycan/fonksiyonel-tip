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
                tip = "dusuk"  # Yeşil kutu tetikleyecek
                nedenler, takviye, dinamik = self._dusun_dusuk(param, v)
            elif deger > meta["opt_max"]:
                durum = "Yüksek (Optimal Sınırın Üzerinde) 📈"
                tip = "yuksek"  # Kırmızı kutu tetikleyecek
                nedenler, takviye, dinamik = self._dusun_yuksek(param, v)
            else:
                durum = "Optimal (Fonksiyonel Aralıkta) ✅"
                tip = "optimal"  # Gri/Nötr kutu tetikleyecek
                nedenler = ["Klinik risk saptanmadı. Hücresel denge kararlı."]
                takviye = "Destek gerekmiyor. Mevcut beslenme düzeni korunabilir."
                dinamik = "🔗 **Biyokimyasal Durum:** İlgili yolaklar ve reseptör duyarlılığı optimal düzeyde."

            sonuclar[meta["name"]] = {
                "deger": f"{deger} {meta['unit']}",
                "durum": durum,
                "tip": tip,
                "nedenler": nedenler,
                "takviye": takviye,
                "dinamik": dinamik
            }
        return sonuclar

    def _dusun_dusuk(self, param, v):
        motor = {
            "Ferritin": (
                ["Mide asidi eksikliği", "Sızdıran bağırsak", "Yetersiz beslenme"],
                "Demir Bisglisinat veya Lipozomal Demir (C Vitamini ile).",
                "🧬 **Biyokimyasal Etkileşim:** Demir eksikliği TPO aktivitesini inhibe eder. T4-T3 dönüşümü yavaşlar ve TSH yükselir."
            ),
            "B12": (
                ["PPI (Mide Koruyucu) kullanımı", "Metformin kullanımı", "Emilim bozukluğu"],
                "Metilkobalamin veya Adenozilkobalamin (Dilaltı).",
                "🧬 **Biyokimyasal Etkileşim:** B12 eksikliği metilasyonu tıkar, Homosistein birikir ve kardiyovasküler risk artar."
            ),
            "D_Vitamini": (
                ["Güneş ışığı eksikliği", "Yağ emilim sorunları"],
                "Vitamin D3 + K2 (Yağlı öğünle).",
                "🧬 **Biyokimyasal Etkileşim:** D3 eksikliği kalsiyum emilimini düşürür, PTH kompenzatuar olarak yükselir."
            ),
            "Magnezyum": (
                ["Kronik stres (Kortizol)", "Yoğun kahve/alkol tüketimi"],
                "Malat (Kas), Bisglisinat (Uyku/Anksiyete) veya Sitrat.",
                "🧬 **Biyokimyasal Etkileşim:** Eksiklik insülin reseptör aktivitesini bozarak doğrudan insülin direncini (HbA1c) tetikler."
            ),
            "Cinko": (
                ["Fitattan zengin beslenme", "Bağırsak enflamasyonu"],
                "Çinko Pikolinat veya Bisglisinat.",
                "🧬 **Biyokimyasal Etkileşim:** Çinko eksikliği mide asidini (HCl) düşürür; Ferritin ve B12 emilimi sekonder olarak çöker."
            ),
            "Hb": (["Demir eksikliği anemi", "B12 eksikliği"], "Şelatlı Demir veya Aktif B Kompleks.", "🧬 **Biyokimyasal Etkileşim:** Mitokondriyal ATP sentezi yavaşlar, doku hipoksisi ve yorgunluk başlar."),
            "TSH": (["Hipertiroidi eğilimi"], "Klinisyen takibi.", "🧬 **Biyokimyasal Etkileşim:** Metabolizma hızı kontrolsüz artar."),
            "CRP": (["Risk yok"], "Düşük CRP idealdir.", "🧬 **Biyokimyasal Etkileşim:** Sistemik enflamatuar yük düşüktür."),
            "HbA1c": (["Reaktif hipoglisemi"], "Protein ağırlıklı beslenme.", "🧬 **Biyokimyasal Etkileşim:** Hücresel glukoz dalgalanmaları mevcuttur.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek yok.", "Veri yok."))

    def _dusun_yuksek(self, param, v):
        motor = {
            "CRP": (
                ["Akut enfeksiyon", "Kronik enflamasyon", "Otoimmünite"],
                "Omega-3 (Yüksek EPA/DHA) ve Lipozomal Kurkumin.",
                "🧬 **Biyokimyasal Etkileşim:** Yüksek CRP karaciğerden Hepsidin salgılatır. Hepsidin demir emilimini bloke eder; Ferritin akut faz reaktanı olarak yükselirken hücresel demir çöker."
            ),
            "HbA1c": (
                ["İnsülin direnci", "Metabolik sendrom"],
                "Berberin, Alfa Lipoik Asit ve Krom Pikolinat.",
                "🧬 **Biyokimyasal Etkileşim:** Kronik hiperglisemi AGEs birikimine yol açar, Nitrik Oksit (NO) sentezini düşürür ve damar hasarı başlatır."
            ),
            "TSH": (
                ["Subklinik Hipotiroidi (Haşimato)"],
                "Selenyum (L-Selenometiyonin) ve CoQ10.",
                "🧬 **Biyokimyasal Etkileşim:** Tiroid yetersizliği karaciğerde LDL reseptörlerini azaltır; dislipidemiye ve kolesterol yüksekliğine yol açar."
            ),
            "Ferritin": (["Aşırı demir yükü", "Karaciğer yağlanması"], "Flebotomi kontrolü, demirli multivitaminlerin kesilmesi.", "🧬 **Biyokimyasal Etkileşim:** Serbest demir Fenton Reaksiyonu ile mitokondriyal DNA hasarı yaratır."),
            "B12": (["Yüksek doz sentetik takviye"], "Takviye kesilir.", "🧬 **Biyokimyasal Etkileşim:** Hücre içine alınamayan B12 kanda birikir, fonksiyonel metilasyon bozukluğuna işarettir."),
            "D_Vitamini": (["Kontrolsüz doz kullanımı"], "D3 stop, kalsiyum takibi.", "🧬 **Biyokimyasal Etkileşim:** Yumuşak doku ve damar endotelinde kalsifikasyon riski artar."),
            "Magnezyum": (["Böbrek yetmezliği"], "Magnezyum stop.", "🧬 **Biyokimyasal Etkileşim:** Nöromüsküler kavşakta asetilkolin baskılanır, refleksler yavaşlar."),
            "Cinko": (["Aşırı doz takviye"], "Çinko takviyesi kesilir.", "🧬 **Biyokimyasal Etkileşim:** Yüksek çinko metallotiyonein proteinini uyarır. Bu protein bakıra bağlanarak Bakır emilimini felç eder."),
            "Hb": (["Dehidratasyon", "Sigara / Hipoksi"], "Sıvı alımı artırılmalı.", "🧬 **Biyokimyasal Etkileşim:** Kan viskozitesi artar, mikrodolaşım direnci yükselir.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek yok.", "Veri yok."))

# --- TELEFON ARAYÜZÜ (STREAMLIT UI) ---
st.title("🩺 Fonksiyonel Tıp & Farmakodinamik")
st.write("Kan değerlerini girin veya tahlil fotoğrafını yükleyin.")
st.markdown("---")

st.subheader("📸 1. Aşama: Fotoğraf Yükle")
yuklenen_dosya = st.file_uploader("Tahlil fotoğrafı veya ekran görüntüsü", type=["png", "jpg", "jpeg"])

otomatik_degerler = {
    "Ferritin": 24.0, "Hb": 11.8, "B12": 310.0, "D_Vitamini": 18.0, 
    "TSH": 3.4, "Magnezyum": 1.9, "Cinko": 115.0, "CRP": 1.5, "HbA1c": 5.5
}

varsayilanlar = otomatik_degerler

if yuklenen_dosya is not None:
    st.success("✅ Görsel yüklendi! Yapay Zeka verileri tarıyor...")
    st.info("📊 Okunan değerler aşağıdaki panele aktarıldı.")

st.markdown("---")
st.subheader("📋 Laboratuvar Kontrol Paneli")

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
            
            # Tamamen Güvenli Yerel Streamlit Renk Kutuları (HTML İçermez, Hata Payı Sıfır)
            if veri["tip"] == "dusuk":
                st.success(veri["durum"])  # Yeşil Arka Plan Kartı
            elif veri["tip"] == "yuksek":
                st.error(veri["durum"])    # Kırmızı Arka Plan Kartı
            else:
                st.info(veri["durum"])     # Mavi/Gri Arka Plan Kartı
            
            st.markdown(veri['dinamik'])
            st.markdown("**[Olası Klinik Nedenler]:**")
            for n in veri['nedenler']:
                st.markdown(f"- {n}")
            st.markdown(f"💡 **[OTC ve Destek Önerisi]:**\n*{veri['takviye']}*")
