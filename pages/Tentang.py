import streamlit as st

st.set_page_config(page_title="Tentang", page_icon="📖")
st.markdown("<h1 style='color:#FF69B4;'>📖 Tentang Aplikasi</h1>", unsafe_allow_html=True)

st.markdown("""
Aplikasi Cuaca Indonesia ini dirancang untuk memberikan informasi cuaca secara real-time berdasarkan kota yang kamu pilih.

💡 **Fitur Utama:**
- Pilihan input kota via dropdown/manual
- Auto-saran untuk nama kota jika typo
- Info cuaca harian (suhu, kelembapan, angin, UV Index, AQI)
- Grafik prakiraan suhu 5 hari ke depan
- Tips cuaca harian
- Unduhan data cuaca
- Mobile-friendly layout

🛠️ **Cara Kerja:**
Data diambil melalui API dari [OpenWeatherMap](https://openweathermap.org/) menggunakan kota yang dipilih, kemudian divisualisasikan menggunakan Streamlit.

🎓 **Tim Mahasiswa Kelompok 5:**
- Difta Alzena Sakhi — 23083010061  
- Steffany Marcellia Witanto — 23083010046  
- Jacinda Ardina Gestyaki — 23083010041  
- Ester Yunita Nainggolan — 23083010039  
- Rosyidatul Kamila — 23083010076

📃 **Lisensi:**
Proyek ini dikembangkan untuk keperluan pembelajaran dan tugas akhir Mata Kuliah Komputasi Awan. Semua data cuaca berasal dari OpenWeatherMap.
""")
