import requests
import folium

# Renk kodları (risk seviyelerine göre)
renk_kodlari = {"YÜKSEK": "red", "ORTA": "orange", "DÜŞÜK": "green"}

# Haritaya eklenecek iller ve koordinatları
iller = {
    "Antalya":     {"lat": 36.8969, "lon": 30.7133},
    "Muğla":       {"lat": 37.2153, "lon": 28.3636},
    "Adana":       {"lat": 37.0000, "lon": 35.3213},
    "İzmir":       {"lat": 38.4192, "lon": 27.1287},
    "Balıkesir":   {"lat": 39.6484, "lon": 27.8826},
    "Karabük":     {"lat": 41.2061, "lon": 32.6204},
    "Bursa":       {"lat": 40.1828, "lon": 29.0663},
    "Eskişehir":   {"lat": 39.7667, "lon": 30.5256},
    "Niğde":       {"lat": 37.9667, "lon": 34.6833},
    "Mersin":      {"lat": 36.8000, "lon": 34.6333},
    "Hatay":       {"lat": 36.2020, "lon": 36.1600},
    "Kahramanmaraş":{"lat": 37.5736, "lon": 36.9371},
    "Osmaniye":    {"lat": 37.0742, "lon": 36.2472},
    "Aydın":       {"lat": 37.8450, "lon": 27.8396},
    "Denizli":     {"lat": 37.7765, "lon": 29.0864},
    "Manisa":      {"lat": 38.6191, "lon": 27.4289},
    "Şanlıurfa":   {"lat": 37.1591, "lon": 38.7969}
}

# Türkiye ortasında başlatılan harita
harita = folium.Map(location=[38.5, 32.0], zoom_start=6)

for sehir, konum in iller.items():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={konum['lat']}&longitude={konum['lon']}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    try:
        weather = data["current_weather"]
        sicaklik = weather["temperature"]
        ruzgar = weather["windspeed"]
        nem = 30  # Open-Meteo current_weather'da nem yok, varsayılan değer

        # Risk hesapla
        if sicaklik > 35 and nem < 25 and ruzgar > 5:
            risk = "YÜKSEK"
        elif sicaklik > 32 and nem < 35:
            risk = "ORTA"
        else:
            risk = "DÜŞÜK"

        # Haritaya işaretçi ekle
        folium.Marker(
            location=[konum["lat"], konum["lon"]],
            popup=f"{sehir}\n🌡️ {sicaklik}°C\n🌬️ {ruzgar} m/s\n🔥 Risk: {risk}",
            icon=folium.Icon(color=renk_kodlari[risk])
        ).add_to(harita)

    except Exception as e:
        print(f"⚠️ {sehir} için veri alınamadı: {e}")

# HTML dosyasını kaydet
harita.save("turkiye_yangin_risk_harita.html")
print("✅ Harita başarıyla güncellendi.")
