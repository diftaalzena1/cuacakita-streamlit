import streamlit as st 
import requests
import pandas as pd
from datetime import datetime
import pytz
import plotly.express as px

API_KEY = "bee15fe1d7bb08020c0757e45d91179a"

@st.cache_data(show_spinner=False)
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

@st.cache_data(show_spinner=False)
def get_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

@st.cache_data(show_spinner=False)
def get_uv_index(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url).json()

@st.cache_data(show_spinner=False)
def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url).json()

# Judul halaman
st.markdown("<h1 style='color:#FF69B4;'>🌈 Cuaca Hari Ini</h1>", unsafe_allow_html=True)

# Validasi input kota
if "selected_city" not in st.session_state:
    st.warning("⚠️ Silakan pilih kota terlebih dahulu dari halaman Home.")
    st.stop()

city = st.session_state.selected_city
res = get_weather_data(city)

if "main" in res:
    lat, lon = res["coord"]["lat"], res["coord"]["lon"]
    uv = get_uv_index(lat, lon)
    aqi = get_air_quality(lat, lon)

    # Mapping interpretasi AQI
    aqi_map = {
        1: "Baik",
        2: "Sedang",
        3: "Tidak Sehat bagi Kelompok Sensitif",
        4: "Tidak Sehat",
        5: "Sangat Tidak Sehat"
    }

    aqi_val = aqi.get("list", [{}])[0].get("main", {}).get("aqi", None)
    aqi_text = f"{aqi_val} - {aqi_map.get(aqi_val, 'N/A')}" if aqi_val else "N/A"

    suhu = res['main']['temp']
    if suhu > 30:
        mood = "🥵 Panas Banget!"
    elif suhu > 25:
        mood = "🌞 Hangat"
    elif suhu > 18:
        mood = "🌤️ Sejuk"
    else:
        mood = "❄️ Dingin"

    weather = {
        "Suhu": f"{suhu}°C",
        "Cuaca": res['weather'][0]['description'].title(),
        "Kelembapan": f"{res['main']['humidity']}%",
        "Angin": f"{res['wind']['speed']} m/s arah {res['wind'].get('deg', 0)}°",
        "UV Index": uv.get("value", "N/A"),
        "AQI": aqi_text
    }

    st.image(f"http://openweathermap.org/img/wn/{res['weather'][0]['icon']}@2x.png")
    st.markdown(f"<h3 style='font-size:20px;'>📍 {res['name']} - {datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%A, %d %B %Y %H:%M WIB')}</h3>", unsafe_allow_html=True)
    st.markdown(f"📌 Koordinat: **{lat}, {lon}**")
    st.markdown(f"**Mood Suhu**: {mood}")
    st.table(pd.DataFrame(weather.items(), columns=["Parameter", "Nilai"]))

    # Grafik suhu 5 hari
    forecast_data = get_forecast(lat, lon)
    df = pd.DataFrame([
        {
            "Waktu": item["dt_txt"],
            "Suhu": item["main"]["temp"],
            "Cuaca": item["weather"][0]["main"]
        }
        for item in forecast_data["list"]
    ])

    fig = px.line(df, x="Waktu", y="Suhu", title="📈 Grafik Prakiraan Suhu 5 Hari", markers=True,
                  line_shape='linear', color_discrete_sequence=["#FF69B4"])
    fig.update_traces(marker=dict(color="#FF69B4", size=6))
    st.plotly_chart(fig, use_container_width=True)

    # Tips berdasarkan kondisi
    tips = {
        "Rain": "☔ Bawa payung atau jas hujan.",
        "Clear": "😎 Cuaca cerah, cocok untuk aktivitas luar!",
        "Clouds": "☁️ Mendung, jangan lupa tetap semangat.",
        "Snow": "🧥 Dinginnya menusuk, pakai pakaian hangat.",
        "Drizzle": "🌦️ Gerimis, hati-hati di jalan.",
    }
    kondisi = res['weather'][0]['main']
    saran = tips.get(kondisi, "✨ Tetap jaga kesehatan dan ikuti prakiraan cuaca!")
    st.markdown(f"### 💡 Tips Harian: {saran}")

    # Unduh CSV
    st.download_button(
        label="⬇️ Unduh Data Cuaca",
        data=pd.DataFrame([weather]).to_csv(index=False),
        file_name=f"cuaca_{res['name']}.csv",
        mime="text/csv"
    )
else:
    st.error("😥 Data cuaca tidak ditemukan.")

st.caption("📡 Powered by OpenWeatherMap | Tim Cuaca Kelompok 5 💖")