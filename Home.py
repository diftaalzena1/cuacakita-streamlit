import streamlit as st
import json
import random
from datetime import datetime
import pytz
import difflib

# Konfigurasi halaman
st.set_page_config(page_title="Beranda Cuaca Indonesia", page_icon="☀️")

# Judul dinamis dengan emoji cuaca acak
emoji = random.choice(["🌧️", "🌞", "🌦️", "🌈", "☀️", "🌫️"])
st.markdown(f"<h1 style='color:#FF69B4;'>{emoji} Selamat Datang di <i>CuacaKita</i></h1>", unsafe_allow_html=True)
st.markdown("<p><i>Pantau cuaca terkini di berbagai wilayah Indonesia — dari kota besar hingga pelosok desa 🌏</i></p>", unsafe_allow_html=True)

# Load data mapping provinsi-kota
with open("provinsi_kota_mapping.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)

# Filter provinsi valid
valid_provinces = [prov for prov in all_data if prov not in ["Tidak diketahui", "Gagal Ambil"]]

# Buat dictionary untuk pencarian manual (pakai lowercase biar mudah dicocokkan)
city_coord_map = {
    city["name"].lower(): {
        "id": city["id"],
        "coord": city["coord"]
    }
    for prov in valid_provinces for city in all_data[prov]
}

# Input kota
st.markdown("### Pilih Metode Input Kota")
input_mode = st.radio("Metode input", ["Dropdown", "Manual"])
city = None

if input_mode == "Dropdown":
    province = st.selectbox("Pilih Provinsi", valid_provinces)
    city_list = [kota["name"] for kota in all_data[province]]
    city = st.selectbox("Pilih Kabupaten/Kota", city_list)

else:
    manual_input = st.text_input("Masukkan Nama Kabupaten/Kota (contoh: Surabaya)")
    if manual_input:
        if manual_input.lower() in city_coord_map:
            city = manual_input
        else:
            saran = difflib.get_close_matches(manual_input.lower(), city_coord_map.keys(), n=1)
            if saran:
                st.info(f"Mungkin maksudmu: **{saran[0].title()}**")
            st.warning("❗ Nama kota tidak ditemukan")

# Jika kota valid dipilih, simpan ke session state
if city:
    st.session_state.selected_city = city
    emojis = ["☀️", "🌤️", "⛅", "🌦️", "🌧️", "⛈️", "🌩️"]
    st.success(f"✅ Kota berhasil dipilih: **{city.title()}** {random.choice(emojis)}")
    st.info("➡️ Silakan buka halaman *Cuaca* dari sidebar untuk melihat informasi cuaca lengkap.")

# Tampilkan waktu saat ini di WIB
wib_time = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%A, %d %B %Y - %H:%M WIB")
st.markdown(f"🕒 Waktu saat ini: **{wib_time}**")

# Footer
st.caption("📌 Data cuaca bersumber dari OpenWeatherMap.")
