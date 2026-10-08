# Bike Sharing Data Analysis

## Deskripsi
Proyek analisis data akhir (Dicoding, kelas Data Analysis) yang menganalisis pola penyewaan sepeda berdasarkan **jam, tipe hari, cuaca, dan musim**. Alur: Business Questions → Data Wrangling → EDA → Visualisasi → Analisis Lanjutan (manual grouping) → Conclusion & Recommendation, disertai dashboard Streamlit interaktif.

## Dataset
**Bike Sharing Dataset** (Capital Bikeshare, Washington D.C.) — Fanaee-T & Gama (2013). Proyek memakai **dua file** (nama asli dataset: `data_1.csv` = `hour.csv`, `data_2.csv` = `day.csv`; isi tidak diubah): `data/data_1.csv` (17.379 baris per jam; analisis utama) dan `data/data_2.csv` (731 baris per hari; validasi silang dan analisis harian), periode 1 Jan 2011 – 31 Des 2012. Kolom utama: `dteday`, `season`, `hr`, `workingday`, `weathersit`, `temp`, `hum`, `windspeed`, `casual`, `registered`, `cnt`.

## Business Questions
1. Pada jam berapa rata-rata penyewaan per jam mencapai puncak pada *working day* dibandingkan *non-working day*, dan berapa rata-ratanya, selama Jan 2011 – Des 2012?
2. Berapa persen penurunan rata-rata penyewaan per jam pada cuaca buruk (Mist/Cloudy dan Light Rain/Snow) dibandingkan cuaca cerah, dan pada musim apa penurunan akibat hujan/salju paling besar, selama Jan 2011 – Des 2012?

## Insight Utama
- **Working day** berpola komuter: puncak pada jam **17:00 (525,3 sepeda/jam)** dan **08:00 (477,0)**. **Non-working day** berpola rekreasi: puncak landai pada jam **13:00 (372,7)**.
- Dibanding cuaca cerah (204,9), penyewaan turun **±14,5%** saat Mist/Cloudy dan **±45,5%** saat Light Rain/Snow. Dampak hujan/salju terbesar di **Winter (±-51,9%)** dan **Spring (±-50,4%)**, terkecil di **Summer (±-29,7%)**.
- Analisis lanjutan: High Demand (226–977 sewa/jam) paling sering di **Summer (44,8%)**, paling jarang di **Winter (13,6%)**.
- Validasi dengan `data_2.csv`: total harian identik dengan jumlah per jam pada seluruh 731 hari, dan analisis harian memberi arah yang sama untuk BQ2 (Summer paling tahan cuaca basah).
- Catatan kualitas data: label `season` pada dokumentasi (1 = springer) tidak cocok dengan tanggal (kode 1 = Jan–20 Mar & 21–31 Des = musim dingin), sehingga dilabeli ulang berdasarkan bukti tanggal; 165 jam tidak tercatat di `data_1.csv` (kemungkinan jam tanpa penyewaan) dan uji sensitivitas menunjukkan jam puncak tidak berubah.

## Struktur Project
```
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── data_1.csv
│   └── data_2.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard
1. Install Python 3.9+
2. Buka terminal dan masuk ke folder project (`submission/`)
3. (Opsional) buat virtual environment
4. Install dependency:
   ```
   pip install -r requirements.txt
   ```
5. Jalankan:
   ```
   streamlit run dashboard/dashboard.py
   ```

## Dashboard
URL Streamlit Cloud: lihat `url.txt` (diisi setelah deployment).

## Author
M Fahril Luthfi — Sistem Informasi, Universitas Islam Negeri Sultan Syarif Kasim Riau
