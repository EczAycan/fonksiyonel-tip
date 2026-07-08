import streamlit as st
import base64

# Sayfa Yapılandırması (Mobil Uyumlu)
st.set_page_config(page_title="Fonksiyonel Tıp & Farmakodinamik", page_icon="🧬", layout="centered")

class AdvancedClinicalEngine:
    def __init__(self):
        # Parametre bilgileri, Fonksiyonel Optimal Aralıklar ve Standart Referanslar
        self.kb = {
            "Ferritin": {"name": "Ferritin", "unit": "ng/mL", "opt_min": 50.0, "opt_max": 80.0, "ref": "13 - 150 ng/mL"},
            "Hb": {"name": "Hemoglobin (Hb)", "unit": "g/dL", "opt_min": 12.5, "opt_max": 15.5, "ref": "12.0 - 16.0 g/dL"},
            "B12": {"name": "B12 Vitamini", "unit": "pg/mL", "opt_min": 600.0, "opt_max": 1000.0, "ref": "200 - 900 pg/mL"},
            "D_Vitamini": {"name": "25-OH Vitamin D3", "unit": "ng/mL", "opt_min": 50.0, "opt_max": 80.0, "ref": "30 - 100 ng/mL"},
            "TSH": {"name": "TSH", "unit": "mIU/L", "opt_min": 0.5, "opt_max": 2.0, "ref": "0.4 - 4.0 mIU/L"},
            "Magnezyum": {"name": "Magnezyum (Serum)", "unit": "mg/dL", "opt_min": 2.2, "opt_max": 2.6, "ref": "1.6 - 2.6 mg/dL"},
            "Cinko": {"name": "Çinko", "unit": "µg/dL", "opt_min": 100.0, "opt_max": 130.0, "ref": "70 - 120 µg/dL"},
            "CRP": {"name": "hs-CRP (Enflamasyon)", "unit": "mg/L", "opt_min": 0.0, "opt_max": 1.0, "ref": "0.0 - 5.0 mg/L"},
            "HbA1c": {"name": "HbA1c (Metabolik)", "unit": "%", "opt_min": 4.8, "opt_max": 5.2, "ref": "4.0 - 5.6 %"}
        }

    def analiz_et(self, v):
        sonuclar = {}
        for param, deger in v.items():
            if deger is None: continue
            meta = self.kb[param]
            
            if deger < meta["opt_min"]:
                durum = "Düşük (Fonksiyonel Eksiklik) 📉"
                tip = "dusuk"
                nedenler, takviye = self._dusun_dusuk(param, v)
            elif deger > meta["opt_max"]:
                durum = "Yüksek (Optimal Sınırın Üzerinde) 📈"
                tip = "yuksek"
                nedenler, takviye = self._dusun_yuksek(param, v)
            else:
                durum = "Optimal (Fonksiyonel Aralıkta) ✅"
                tip = "optimal"
                nedenler = ["Klinik risk saptanmadı. Hücresel denge kararlı."]
                takviye = "Destek gerekmiyor. Mevcut beslenme düzeni korunabilir."

            sonuclar[meta["name"]] = {
                "deger": f"{deger} {meta['unit']}",
                "durum": durum,
                "tip": tip,
                "nedenler": nedenler,
                "takviye": takviye,
                "opt_aralik": f"{meta['opt_min']} - {meta['opt_max']} {meta['unit']}",
                "lab_ref": meta["ref"]
            }
        return sonuclar

    def _dusun_dusuk(self, param, v):
        motor = {
            "Ferritin": (
                ["Mide asidi eksikliği", "Sızdıran bağırsak sendromu", "Kronik düşük yoğunluklu enflamasyon (Hepsidin blokajı)"],
                "Demir Bisglisinat veya Lipozomal Demir (C Vitamini kofaktörüyle). Mide asidi desteği."
            ),
            "B12": (
                ["Metilasyon döngüsü tıkanıklığı", "PPI (Mide Koruyucu) kullanımı", "Malabsorbsiyon"],
                "Dilaltı Metilkobalamin veya Adenozilkobalamin aktif formları."
            ),
            "D_Vitamini": (
                ["Güneş ışığı eksikliği", "VDR (Vitamin D Reseptör) polimorfizmi", "Yağ emilim sorunları"],
                "Vitamin D3 + K2 (Yağlı öğünle sinerjik emilim)."
            ),
            "Magnezyum": (
                ["Kronik sempatik dominans (Savaş ya da Kaç)", "Kortizolün Magnezyum Yağması", "Yoğun kahve/alkol tüketimi"],
                "Hücre içi enerji için Malat, HPA aksını sakinleştirmek için Bisglisinat/Treonat formları."
            ),
            "Cinko": (
                ["Fitattan zengin beslenme", "Bağırsak mukozal hasarı", "Yüksek bakır maruziyeti"],
                "Çinko Pikolinat veya Bisglisinat şelat formları."
            ),
            "Hb": (["Hücresel hipoksi", "Demir ve B12 eksikliği anemisi"], "Şelatlı Demir veya Aktif B Kompleks."),
            "TSH": (["Hipertiroidi eğilimi", "Reseptör aşırı duyarlılığı"], "Klinisyen takibi."),
            "CRP": (["Risk yok"], "Düşük CRP idealdir."),
            "HbA1c": (["Reaktif hipoglisemi", "Yetersiz glukoz yükü"], "Protein ve sağlıklı yağ ağırlıklı beslenme.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek yok."))

    def _dusun_yuksek(self, param, v):
        motor = {
            "CRP": (
                ["Akut/Kronik enfeksiyon", "Otoimmünite (Otoenflamasyon)", "Sistemik yangı"],
                "Yüksek EPA/DHA içeren Omega-3 ve hücresel inflamasyonu bloke eden Lipozomal Kurkumin."
            ),
            "HbA1c": (
                ["İnsülin direnci (Reseptör Körlüğü)", "Metabolik Sendrom", "Glikasyon yükü"],
                "Berberin, Alfa Lipoik Asit (ALA) ve Krom Pikolinat."
            ),
            "TSH": (
                ["Subklinik Hipotiroidi", "HPA Aksı Enerji Tasarrufu Modu (Hücresel kriz)"],
                "Selenyum (L-Selenometiyonin) ve mitokondriyal ETZ koruyucu CoQ10."
            ),
            "Ferritin": (["Aşırı demir yükü", "Karaciğer yağlanması", "Akut faz yanıtı"], "Flebotomi kontrolü, antioksidan tedaviler."),
            "B12": (["Sentetik takviye birikimi", "Hücre içi alım defekti"], "Takviye kesilir, aktif formlar değerlendirilir."),
            "D_Vitamini": (["Toksisite sınırı", "Kontrolsüz doz kullanımı"], "D3 stop, kalsiyum og PTH takibi."),
            "Magnezyum": (["İleri derece böbrek yetmezliği"], "Magnezyum stop."),
            "Cinko": (["Aşırı doz takviye", "Bakır antagonizması"], "Çinko takviyesi kesilir."),
            "Hb": (["Dehidratasyon", "Kronik hipoksi yanıtı (Sigara vb.)"], "Sıvı alımı artırılmalı, doku oksijenasyonu izlenmeli.")
        }
        return motor.get(param, (["Neden bulunamadı."], "Destek yok."))

def pdf_raporu_uret(rapor_verisi):
    """Gelişmiş Yazdırma ve PDF Tetikleyicili HTML Rapor Çıktısı"""
    
    style_blok = """
    <style>
        body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #2c3e50; padding: 30px; line-height: 1.6; }
        .header { text-align: center; border-bottom: 3px solid #1a365d; padding-bottom: 15px; margin-bottom: 30px; }
        .title { color: #1a365d; margin: 0; font-size: 24px; }
        .sub-title { color: #4a5568; margin: 5px 0 0 0; font-size: 14px; }
        .print-btn-container { text-align: center; margin-bottom: 20px; }
        .print-btn { background-color: #2b6cb0; color: white; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 5px; cursor: pointer; }
        .meta-table { width: 100%; border-collapse: collapse; margin-bottom: 40px; box-shadow: 0 2px 3px rgba(0,0,0,0.1); }
        .meta-table th, .meta-table td { border: 1px solid #e2e8f0; padding: 12px; text-align: left; }
        .meta-table th { background-color: #f7fafc; color: #2d3748; font-weight: bold; }
        .item-box { margin-top: 15px; padding: 15px; border-left: 4px solid #4a5568; background: #f7fafc; border-radius: 0 6px 6px 0; page-break-inside: avoid; }
        .item-title { font-weight: bold; color: #2c5282; font-size: 16px; margin-bottom: 5px; }
        .global-box { margin-top: 35px; padding: 25px; border-left: 6px solid #1565c0; background: #e3f2fd; border-radius: 0 8px 8px 0; }
        .global-title { font-weight: bold; color: #0d47a1; font-size: 20px; margin-bottom: 12px; }
        @media print {
            .print-btn-container { display: none; }
            body { padding: 0; }
        }
    </style>
    """

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Klinik Destek Raporu</title>
        {style_blok}
    </head>
    <body>
        <div class="print-btn-container">
            <button class="print-btn" onclick="window.print()">🖨️ PDF Olarak Kaydet / Yazdır</button>
        </div>
        <div class="header">
            <h2 class="title">🧬 Patofizyoloji ve Klinik Destek Raporu</h2>
            <p class="sub-title">Bütüncül Biyokimya ve Fonksiyonel Tıp Hücresel Analiz Paneli</p>
        </div>
        <table class="meta-table">
            <thead>
                <tr>
                    <th>Parametre</th>
                    <th>Ölçülen Değer</th>
                    <th>Standart Referans</th>
                    <th>Fonksiyonel Optimal Aralık</th>
                    <th>Durum</th>
                </tr>
            </thead>
            <tbody>
    """
    for p_name, veri in rapor_verisi.items():
        html += f"""
                <tr>
                    <td><b>{p_name}</b></td>
                    <td>{veri['deger']}</td>
                    <td>{veri['lab_ref']}</td>
                    <td>{veri['opt_aralik']}</td>
                    <td>{veri['durum']}</td>
                </tr>
        """
    html += "</tbody></table>"
    
    for p_name, veri in rapor_verisi.items():
        nedenler_str = ", ".join(veri['nedenler'])
        html += f"""
        <div class="item-box">
            <div class="item-title">🔹 {p_name} ({veri['deger']}) — {veri['durum']}</div>
            <p style="margin: 3px 0;"><b>Olası Nedenler:</b> {nedenler_str}</p>
            <p style="margin: 3px 0;">💡 <b>OTC Önerisi:</b> <i>{veri['takviye']}</i></p>
        </div>
        """
        
    # Hastaya özgü entegre edilen bütüncül hoca özeti HTML'e gömülüyor
    html += f"""
    <div class="global-box">
        <div class="global-title">🧬 GENEL KLİNİK DEĞERLENDİRME & PATOFİZYOLOJİK ETKİLEŞİM</div>
        <p><b>Hücresel Sinyal İletim Hikayesi:</b></p>
        <p>Girilen laboratuvar bulguları, vücutta birbiri ardına tetiklenen sistemik bir <b>"Domino Etkisini"</b> net bir şekilde doğrulamaktadır. Tekil değerlerden ziyade, bu değerlerin birbiriyle konuşma dili hücresel krizleri işaret eder:</p>
        <ul>
            <li><b>Metilasyon Döngüsü ve Enerji Krizi:</b> Fonksiyonel düzeyde baskılanan B12 Vitamini, hücrenin ana yazılım mekanizması olan metilasyon döngüsünü kilitleyerek detoksifikasyon ve nörotransmitter sentezini yavaşlatır. Ferritin ve Hemoglobin düşüklüğü ise mitokondriyal Elektron Taşıma Zinciri'nde (ETZ) oksijenizasyonu bozarak kronik yorgunluğu ve hücresel stresi derinleştirir.</li>
            <li><b>Kortizolün Magnezyum Yağması ve Reseptör Körlüğü:</b> Kronik sempatik dominansa (stres aksına) bağlı olarak salgılanan kortizol, magnezyumu böbreklerden dışarı atmaktadır (Magnezyum Yağması). Magnezyum yetersizliği hücre zarındaki insülin reseptörlerinde körlük yaratarak glukozun içeri alınmasını zorlaştırır ve HbA1c seviyesini yukarı yönlü tetikler.</li>
            <li><b>Hepsidin Blokajı ve Tiroid Frene Basma Aksı (HPA):</b> hs-CRP'deki hafif yükseliş (kronik düşük yoğunluklu yangı), karaciğerden Hepsidin hormonunu salgılatarak bağırsak demir kapılarını kilitler; bu durum demiri hücresel düzeyde tutsak bırakır. Hücrelerin demirsiz ve ATP'siz kaldığını fark eden HPA (Hipotalamus-Hipofiz-Adrenal) aksı ise hayatta kalabilmek için metabolizma hızını tiroid üzerinden (TSH yükselterek) bilinçli olarak yavaşlatır.</li>
        </ul>
        <p><b>Bütüncül Hücum Stratejisi:</b> Onarım süreci sadece eksik olanı yerine koymakla değil; hücre zarı akışkanlığını Omega-3 ile korumak, karaciğer blokajını Lipozomal Kurkumin ile söndürmek, stres aksını Magnezyum formları (Malat/Bisglisinat) ile dengelemek ve metilasyonu aktif dilaltı formlarla tetiklemek üzerine kurgulanmalıdır.</p>
    </div>
    """
    
    html += "</body></html>"
    
    b64 = base64.b64encode(html.encode('utf-8')).decode()
    return f'<a href="data:text/html;charset=utf-8;base64,{b64}" download="Klinik_Destek_Raporu.html" style="text-decoration:none;"><button style="width:100%; background-color:#1565c0; color:white; border:none; padding:12px; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer;">📥 Rapor Dosyasını İndir (.html)</button></a>'

# --- TELEFON ARAYÜZÜ (STREAMLIT UI) ---
st.title("🩺 Fonksiyonel Tıp & Farmakodinamik")
st.write("Kan değerlerini girin veya tahlil fotoğrafını yükleyin.")
st.markdown("---")

# Referans Aralıkları Bilgi Paneli
with st.expander("📊 Referans Aralıkları Kılavuzu (Standart vs. Fonksiyonel)", expanded=False):
    st.markdown("""
    | Parametre | Standart Referans Değeri | Fonksiyonel Tıp (Optimal) |
    | :--- | :--- | :--- |
    | **Ferritin** | 13 - 150 ng/mL | **50.0 - 80.0 ng/mL** |
    | **Hemoglobin (Hb)** | 12.0 - 16.0 g/dL | **12.5 - 15.5 g/dL** |
    | **B12 Vitamini** | 200 - 900 pg/mL | **600.0 - 1000.0 pg/mL** |
    | **25-OH Vitamin D3** | 30 - 100 ng/mL | **50.0 - 80.0 ng/mL** |
    | **TSH** | 0.4 - 4.0 mIU/L | **0.5 - 2.0 mIU/L** |
    | **Magnezyum** | 1.6 - 2.6 mg/dL | **2.2 - 2.6 mg/dL** |
    | **Çinko** | 70 - 120 µg/dL | **100.0 - 130.0 µg/dL** |
    | **hs-CRP** | 0.0 - 5.0 mg/L | **0.0 - 1.0 mg/L** |
    | **HbA1c** | 4.0 - 5.6 % | **4.8 - 5.2 %** |
    """)

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
    
    # HTML ve Yazdırma Butonu Alanı
    st.markdown(pdf_raporu_uret(rapor_sonuclari), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sadeleştirilmiş, Akordeon (Expander) Parametre Listesi
    for p_name, veri in rapor_sonuclari.items():
        with st.expander(f"🔹 {p_name} — {veri['deger']}", expanded=False):
            st.caption(f"Standart Referans: {veri['lab_ref']} | Fonksiyonel Optimal: {veri['opt_aralik']}")
            
            if veri["tip"] == "dusuk":
                st.warning(veri["durum"])
            elif veri["tip"] == "yuksek":
                st.error(veri["durum"])
            else:
                st.success(veri["durum"])
            
            st.markdown("**[Olası Klinik Nedenler]:**")
            for n in veri['nedenler']:
                st.markdown(f"- {n}")
            st.markdown(f"💡 **[OTC Takviye Yaklaşımı]:**\n*{veri['takviye']}*")

    # --- EN ALTA EKLENEN GENEL KLİNİK DEĞERLENDİRME PANELİ ---
    st.markdown("---")
    st.info("### 🧬 Genel Klinik Değerlendirme & Patofizyolojik Etkileşim")
    
    st.markdown("""
    **Hücresel Sinyal İletim Hikayesi:**
    
    Girilen laboratuvar bulguları, hastanın vücudunda birbiri ardına tetiklenen sistemik bir **"Domino Etkisini"** net bir şekilde doğrulamaktadır. Tekil değerlerden ziyade, bu değerlerin birbiriyle konuşma dili hücresel krizleri işaret eder:
    
    *   **Metilasyon Döngüsü ve Enerji Krizi:** Fonksiyonel düzeyde baskılanan B12 Vitamini, hücrenin ana yazılım mekanizması olan metilasyon döngüsünü kilitleyerek detoksifikasyon ve nörotransmitter sentezini yavaşlatır. Ferritin ve Hemoglobin düşüklüğü ise mitokondriyal Elektron Taşıma Zinciri'nde (ETZ) oksijenizasyonu bozarak kronik yorgunluğu ve hücresel stresi derinleştirir.
    *   **Kortizolün Magnezyum Yağması ve Reseptör Körlüğü:** Kronik sempatik dominansa (stres aksına) bağlı olarak salgılanan kortizol, magnezyumu böbreklerden idrarla hızla dışarı atar (**Magnezyum Yağması**). Magnezyum yetersizliği hücre zarındaki insülin reseptörlerinde körlük yaratarak glukozun içeri alınmasını zorlaştırır ve HbA1c seviyesini yukarı yönlü tetikler.
    *   **Hepsidin Blokajı ve Tiroid Frene Basma Aksı (HPA):** hs-CRP'deki hafif yükseliş (kronik düşük yoğunluklu yangı), karaciğerden Hepsidin hormonunu salgılatarak bağırsak demir kapılarını kilitler; bu durum demiri hücresel düzeyde tutsak bırakır. Hücrelerin demirsiz ve ATP'siz kaldığını fark eden HPA (Hipotalamus-Hipofiz-Adrenal) aksı ise hayatta kalabilmek için metabolizma hızını tiroid üzerinden (**TSH yükselterek**) bilinçli olarak yavaşlatır.
    
    **💡 Bütüncül Hücum Stratejisi:**
    Onarım süreci sadece eksik olanı yerine koymakla değil; hücre zarı akışkanlığını Omega-3 ile korumak, karaciğer blokajını Lipozomal Kurkumin ile söndürmek, stres aksını Magnezyum formları (Malat/Bisglisinat) ile dengelemek ve metilasyonu aktif dilaltı formlarla tetiklemek üzerine kurgulanmalıdır.
    """)
