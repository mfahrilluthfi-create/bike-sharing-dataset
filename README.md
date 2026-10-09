# Bike Sharing Data Analysis

## Deskripsi
Proyek analisis data akhir (Dicoding, kelas Data Analysis) yang menganalisis pola penyewaan sepeda berdasarkan **jam, tipe hari, cuaca, dan musim**. Alur analisis: Business Questions → Data Wrangling (Gathering, Assessing, Cleaning) → EDA → Visualization & Explanatory Analysis → Analisis Lanjutan (manual grouping) → Conclusion & Recommendation. Hasilnya ditampilkan pada dashboard Streamlit interaktif.

## Dataset
**Bike Sharing Dataset** (Capital Bikeshare, Washington D.C.) — Fanaee-T & Gama (2013). Periode 1 Jan 2011 – 31 Des 2012. Dua file di folder `data/`:
- `data/data_1.csv` — data per jam (17.379 baris; nama asli dataset: `hour.csv`), analisis utama.
- `data/data_2.csv` — data harian (731 baris; nama asli dataset: `day.csv`), untuk validasi silang dan analisis tingkat harian.

Isi kedua file tidak diubah; hanya namanya disesuaikan dengan struktur direktori yang disarankan.

## Business Questions
1. **Pola Jam Puncak Penyewaan Sepeda pada Working Day vs Non-Working Day:** Pada jam berapa rata-rata penyewaan per jam mencapai puncak pada *working day* dibandingkan *non-working day*, dan berapa rata-ratanya, selama Jan 2011 – Des 2012?
2. **Dampak Cuaca Buruk dan Musim terhadap Penyewaan Sepeda:** Berapa persen penurunan rata-rata penyewaan per jam pada cuaca buruk (Mist/Cloudy dan Light Rain/Snow) dibandingkan cuaca cerah, dan pada musim apa penurunan akibat hujan/salju paling besar, selama Jan 2011 – Des 2012?

## Insight Utama
- **Working day** berpola komuter: puncak pada jam **17:00 (525,3 sepeda/jam)** dan **08:00 (477,0)**. **Non-working day** berpola rekreasi: puncak landai pada jam **13:00 (372,7)**.
- Dibanding cuaca cerah (204,9), penyewaan turun **±14,5%** saat Mist/Cloudy dan **±45,5%** saat Light Rain/Snow. Dampak hujan/salju terbesar di **Winter (±-51,9%)** dan **Spring (±-50,4%)**, terkecil di **Summer (±-29,7%)**.
- Analisis lanjutan: High Demand (226–977 sewa/jam) paling sering di **Summer (44,8%)**, paling jarang di **Winter (13,6%)**.
- Validasi dengan `data_2.csv`: total harian identik dengan jumlah per jam pada seluruh 731 hari, dan analisis harian memberi arah yang sama untuk Business Question 2.
- Catatan kualitas data: label `season` pada dokumentasi (1 = springer) tidak cocok dengan tanggal (kode 1 = Jan–20 Mar & 21–31 Des = musim dingin), sehingga dilabeli ulang berdasarkan bukti tanggal; 165 jam tidak tercatat di `data_1.csv` (kemungkinan jam tanpa penyewaan) dan uji sensitivitas menunjukkan jam puncak tidak berubah.

## Struktur Project
```
submission/
├── dashboard/
│   ├── main_data.csv      # data bersih hasil notebook (dipakai dashboard)
│   └── dashboard.py       # aplikasi Streamlit
├── data/
│   ├── data_1.csv         # data per jam
│   └── data_2.csv         # data harian
├── notebook.ipynb         # proses analisis data lengkap
├── README.md
├── requirements.txt
└── url.txt                # URL dashboard yang sudah di-deploy
```

## Persyaratan
- Python 3.9 atau lebih baru
- pip (package manager Python)
- Library (lihat `requirements.txt`): NumPy, Pandas, Matplotlib, Seaborn (analisis di notebook), Streamlit, Plotly (dashboard)

## Setup Environment
Disarankan memakai virtual environment agar library proyek ini tidak bercampur dengan proyek lain.

1. Buka terminal (Command Prompt/PowerShell di Windows, Terminal di macOS/Linux) lalu masuk ke folder proyek:
   ```
   cd submission
   ```
2. Buat virtual environment:
   ```
   python -m venv .venv
   ```
3. Aktifkan virtual environment:
   - Windows:
     ```
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source .venv/bin/activate
     ```
   Jika berhasil, nama `(.venv)` muncul di awal baris terminal.

## Instalasi Dependency
Dengan virtual environment aktif dan berada di folder `submission/`:
```
pip install -r requirements.txt
```

## Menjalankan Dashboard
Masuk ke folder dashboard lalu jalankan Streamlit:
```
cd dashboard
streamlit run dashboard.py
```
Browser akan terbuka otomatis. Jika tidak, buka alamat yang tampil di terminal (biasanya `http://localhost:8501`). Untuk menghentikan dashboard, tekan `Ctrl+C` di terminal.

Alternatif dari folder `submission/` (tanpa `cd dashboard`):
```
streamlit run dashboard/dashboard.py
```

## Menjalankan Notebook (opsional)
Buka `notebook.ipynb` di Jupyter Notebook/Google Colab, lalu pilih *Restart & Run All*. Pastikan folder `data/` berada di sebelah notebook. Jalankan notebook dari folder `submission/`.

## Dashboard Online
https://bike-sharing-dataset-ead24wbk9qtg6azwki5fyc.streamlit.app/

## Fitur Dashboard
**Visualisasi untuk dua Business Questions**
- **Business Question 1 (tab "BQ1: Pola Jam"):** grafik garis rata-rata penyewaan per jam untuk *Working Day* vs *Non-Working Day*, beserta insight jam puncak.
- **Business Question 2 (tab "BQ2: Cuaca & Musim"):** grafik batang rata-rata penyewaan per kondisi cuaca, heatmap musim × cuaca, dan grafik batang penurunan penyewaan saat Light Rain/Snow dibanding cuaca cerah per musim.

**Visualisasi pendukung**
- Tab "Kategori Demand": distribusi dan komposisi Low / Medium / High Demand (hasil analisis lanjutan di notebook).
- Tab "Validasi Harian (data_2.csv)": rata-rata penyewaan harian per cuaca dan tren per bulan.

**Fitur interaktif (filter di sidebar)**
- **Periode tanggal** (pemilih rentang tanggal)
- **Musim** (pilihan ganda)
- **Kondisi cuaca** (pilihan ganda)
- **Tipe hari** (Working Day / Non-Working Day)
- **Rentang jam** (slider 0–23)

Perubahan filter langsung memperbarui KPI (total penyewaan, rata-rata per jam, jam puncak, porsi High Demand), seluruh grafik, dan teks insight.

## Author
M Fahril Luthfi — Sistem Informasi, Universitas Islam Negeri Sultan Syarif Kasim Riau
