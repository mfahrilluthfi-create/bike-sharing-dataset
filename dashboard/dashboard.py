"""Dashboard Bike Sharing: Streamlit.

Membaca dashboard/main_data.csv (data bersih hasil notebook.ipynb), sehingga angka,
label, dan kategori demand (Low / Medium / High Demand) identik dengan notebook.
Jalankan dari folder project:  streamlit run dashboard/dashboard.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------- konfigurasi
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

DATA_PATH = Path(__file__).resolve().parent / "main_data.csv"          # hasil cleaning data_1.csv
DAY_PATH = Path(__file__).resolve().parent.parent / "data" / "data_2.csv"  # data harian asli (data/data_2.csv)
SEASONS = ["Winter", "Spring", "Summer", "Fall"]
WEATHERS = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow/Fog"]
DEMAND = ["Low Demand", "Medium Demand", "High Demand"]
BQ1_TITLE = "Pola Jam Puncak Penyewaan Sepeda pada Working Day vs Non-Working Day"
BQ1_TEXT = "Pada jam berapa rata-rata penyewaan sepeda per jam mencapai puncak pada *working day* dibandingkan *non-working day*, dan berapa rata-rata penyewaan pada jam puncak tersebut, selama periode Januari 2011 – Desember 2012, sehingga operator dapat menjadwalkan redistribusi dan ketersediaan sepeda pada jam-jam kritis?"
BQ2_TITLE = "Dampak Cuaca Buruk dan Musim terhadap Penyewaan Sepeda"
BQ2_TEXT = "Berapa persen penurunan rata-rata penyewaan sepeda per jam pada kondisi cuaca buruk (*Mist/Cloudy* dan *Light Rain/Snow*) dibandingkan cuaca cerah, dan pada musim apa penurunan akibat hujan/salju paling besar, selama Januari 2011 – Desember 2012, sehingga operator dapat menyusun strategi promosi dan perawatan armada berdasarkan musim dan cuaca?"
DAY_COLORS = {"Working Day": "#1f77b4", "Non-Working Day": "#ff7f0e"}
DEMAND_COLORS = {"Low Demand": "#9ecae1", "Medium Demand": "#4292c6", "High Demand": "#08519c"}


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["dteday"])
    df["season_label"] = pd.Categorical(df["season_label"], categories=SEASONS, ordered=True)
    df["weather_label"] = pd.Categorical(df["weather_label"], categories=WEATHERS, ordered=True)
    df["demand_category"] = pd.Categorical(df["demand_category"], categories=DEMAND, ordered=True)
    return df


@st.cache_data
def load_day() -> pd.DataFrame:
    d = pd.read_csv(DAY_PATH, parse_dates=["dteday"])
    # Pembersihan yang sama dengan notebook: label musim berdasarkan bukti tanggal, label cuaca & tipe hari
    d["season_label"] = d["season"].map({1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"})
    d["weather_label"] = d["weathersit"].map(dict(zip([1, 2, 3, 4], WEATHERS)))
    d["day_type"] = d["workingday"].map({1: "Working Day", 0: "Non-Working Day"})
    d["year"] = d["yr"].map({0: 2011, 1: 2012})
    d["season_label"] = pd.Categorical(d["season_label"], categories=SEASONS, ordered=True)
    d["weather_label"] = pd.Categorical(d["weather_label"], categories=WEATHERS, ordered=True)
    return d


df = load_data()
daily = load_day()

# Ringkasan pada DATA PENUH (tanpa filter), dihitung dari main_data.csv; dipakai sebagai pembanding pada insight.
_full_hourly = df.groupby(["day_type", "hr"], observed=True)["cnt"].mean()
FULL_PEAKS = {d: (int(_full_hourly[d].idxmax()), float(_full_hourly[d].max())) for d in DAY_COLORS}
_full_sw = df.pivot_table(index="season_label", columns="weather_label", values="cnt", aggfunc="mean", observed=True)
FULL_DROP = (_full_sw["Light Rain/Snow"] / _full_sw["Clear/Partly Cloudy"] - 1) * 100

# ---------------------------------------------------------------- header
st.title("🚲 Bike Sharing Dashboard")
st.caption(
    "Analisis penyewaan sepeda Capital Bikeshare (Washington D.C.), data per jam "
    f"{df['dteday'].min():%d %b %Y} – {df['dteday'].max():%d %b %Y}. "
    "Dashboard ini memakai data bersih dan kategori yang sama dengan notebook analisis."
)

with st.expander("Dataset overview"):
    c1, c2, c3 = st.columns(3)
    c1.metric("Jumlah baris (jam)", f"{len(df):,}")
    c2.metric("Jumlah hari", f"{df['dteday'].nunique():,}")
    c3.metric("Total penyewaan", f"{int(df['cnt'].sum()):,}")
    st.caption(
        "Sumber data: `data_1.csv` (analisis utama) dan `data_2.csv` (validasi silang). "
        "Catatan: 165 jam tidak tercatat di data per jam (kemungkinan jam tanpa penyewaan; total harian tetap cocok "
        "dengan data_2.csv). Pada uji sensitivitas di notebook, jam puncak tidak berubah."
    )
    bounds = df.groupby("demand_category", observed=True)["cnt"].agg(["min", "max"])
    st.write(
        "Batas kategori demand (kuantil/tertile pada `cnt`, dari notebook): "
        + ", ".join(f"**{k}** = {int(v['min'])}–{int(v['max'])}" for k, v in bounds.iterrows())
        + " penyewaan per jam."
    )
    st.dataframe(df.head(10), width="stretch")

# ---------------------------------------------------------------- filter
st.sidebar.header("Filter")
min_d, max_d = df["dteday"].min().date(), df["dteday"].max().date()
date_range = st.sidebar.date_input("Periode tanggal", (min_d, max_d), min_value=min_d, max_value=max_d)
sel_seasons = st.sidebar.multiselect("Musim", SEASONS, default=SEASONS)
sel_weathers = st.sidebar.multiselect("Kondisi cuaca", WEATHERS, default=WEATHERS)
sel_days = st.sidebar.multiselect("Tipe hari", list(DAY_COLORS), default=list(DAY_COLORS))
hr_min, hr_max = st.sidebar.slider("Rentang jam", 0, 23, (0, 23))

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Pilih tanggal awal dan tanggal akhir pada filter periode.")
    st.stop()

mask = (
    (df["dteday"].dt.date >= date_range[0])
    & (df["dteday"].dt.date <= date_range[1])
    & df["season_label"].isin(sel_seasons)
    & df["weather_label"].isin(sel_weathers)
    & df["day_type"].isin(sel_days)
    & df["hr"].between(hr_min, hr_max)
)
fdf = df[mask]
if fdf.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Longgarkan filter di sidebar.")
    st.stop()

# ---------------------------------------------------------------- KPI
hourly_mean = fdf.groupby("hr")["cnt"].mean()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total penyewaan", f"{int(fdf['cnt'].sum()):,}")
k2.metric("Rata-rata per jam", f"{fdf['cnt'].mean():.1f}")
k3.metric("Jam puncak (rata-rata)", f"{hourly_mean.idxmax():02d}:00", f"{hourly_mean.max():.0f} sepeda/jam", delta_color="off")
k4.metric("Porsi High Demand", f"{(fdf['demand_category'] == 'High Demand').mean() * 100:.1f}%")
st.caption("💡 Semua grafik dan KPI bersifat interaktif: ubah filter periode, musim, cuaca, tipe hari, dan rentang jam di sidebar kiri.")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["⏰ BQ1: Pola Jam", "🌦️ BQ2: Cuaca & Musim", "📊 Kategori Demand", "📅 Validasi Harian (data_2.csv)"])

# ---------------------------------------------------------------- BQ1
with tab1:
    st.subheader(f"Business Question 1: {BQ1_TITLE}")
    st.markdown(f"**Pertanyaan bisnis:** {BQ1_TEXT}")
    hd = fdf.groupby(["hr", "day_type"], observed=True)["cnt"].mean().reset_index()
    fig = px.line(hd, x="hr", y="cnt", color="day_type", markers=True, color_discrete_map=DAY_COLORS,
                  labels={"hr": "Jam dalam sehari (0-23)", "cnt": "Rata-rata penyewaan per jam (unit sepeda)", "day_type": "Tipe hari"})
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig)

    parts = []
    for dtp, g in hd.groupby("day_type"):
        top = g.loc[g["cnt"].idxmax()]
        parts.append(f"**{dtp}**: puncak pada jam **{int(top['hr']):02d}:00** (rata-rata **{top['cnt']:.1f}** sepeda/jam)")
    st.info("**Insight (sesuai filter):** " + "; ".join(parts) + ". "
            "Pada data penuh (tanpa filter): " + "; ".join(f"**{d}** puncak jam **{h:02d}:00** ({v:.1f} sepeda/jam)" for d, (h, v) in FULL_PEAKS.items()) + ".")

# ---------------------------------------------------------------- BQ2
with tab2:
    st.subheader(f"Business Question 2: {BQ2_TITLE}")
    st.markdown(f"**Pertanyaan bisnis:** {BQ2_TEXT}")
    left, right = st.columns(2)

    wd = fdf.groupby("weather_label", observed=True)["cnt"].agg(rata_rata="mean", n="count").reset_index()
    wd["weather_label"] = wd["weather_label"].astype(str)
    fig_w = px.bar(wd, x="weather_label", y="rata_rata", text=wd["rata_rata"].round(1), color="weather_label",
                   color_discrete_map=dict(zip(WEATHERS, ["#2ca02c", "#bcbd22", "#d62728", "#c7c7c7"])),
                   labels={"weather_label": "Kondisi cuaca", "rata_rata": "Rata-rata penyewaan per jam (unit sepeda)"})
    fig_w.update_layout(showlegend=False, title="Rata-rata per kondisi cuaca")
    left.plotly_chart(fig_w)

    sw = fdf.pivot_table(index="season_label", columns="weather_label", values="cnt", aggfunc="mean", observed=True)
    fig_h = px.imshow(sw.round(0), text_auto=True, color_continuous_scale="YlGnBu", aspect="auto",
                      labels={"x": "Kondisi cuaca", "y": "Musim", "color": "Rata-rata/jam"})
    fig_h.update_layout(title="Rata-rata per musim x cuaca")
    right.plotly_chart(fig_h)

    # Grafik penurunan Light Rain/Snow vs cuaca cerah per musim (menjawab "musim apa paling besar")
    if {"Clear/Partly Cloudy", "Light Rain/Snow"}.issubset(sw.columns):
        drop_f = ((sw["Light Rain/Snow"] / sw["Clear/Partly Cloudy"] - 1) * 100).dropna().reset_index()
        drop_f.columns = ["season_label", "selisih"]
        drop_f["season_label"] = drop_f["season_label"].astype(str)
        if not drop_f.empty:
            fig_d2 = px.bar(drop_f, x="season_label", y="selisih", text=drop_f["selisih"].round(1), color_discrete_sequence=["#d62728"],
                            labels={"season_label": "Musim", "selisih": "Selisih terhadap cuaca cerah (%)"})
            fig_d2.update_layout(title="Penurunan rata-rata penyewaan saat Light Rain/Snow vs cuaca cerah, per musim")
            st.plotly_chart(fig_d2)
        else:
            st.caption("Data cuaca cerah dan Light Rain/Snow belum tersedia untuk musim terpilih.")
    else:
        st.caption("Pilih cuaca 'Clear/Partly Cloudy' dan 'Light Rain/Snow' pada filter untuk melihat grafik penurunan per musim.")

    msgs = []
    base = wd.loc[wd["weather_label"] == "Clear/Partly Cloudy", "rata_rata"]
    if not base.empty:
        for w in ["Mist/Cloudy", "Light Rain/Snow"]:
            row = wd.loc[wd["weather_label"] == w, "rata_rata"]
            if not row.empty:
                msgs.append(f"**{w}** {row.iloc[0]:.1f} vs cuaca cerah {base.iloc[0]:.1f} sepeda/jam ({(row.iloc[0] / base.iloc[0] - 1) * 100:+.1f}%)")
    st.info("**Insight (sesuai filter):** " + ("; ".join(msgs) if msgs else "pilih cuaca 'Clear/Partly Cloudy' bersama kondisi lain untuk melihat persentase penurunan") + ". "
            f"Pada data penuh, penurunan akibat Light Rain/Snow paling besar di **{FULL_DROP.idxmin()}** ({FULL_DROP.min():.1f}%) dan paling kecil di **{FULL_DROP.idxmax()}** ({FULL_DROP.max():.1f}%).")
    if (wd["weather_label"] == "Heavy Rain/Snow/Fog").any():
        st.caption("⚠️ Heavy Rain/Snow/Fog hanya 3 baris pada seluruh data: tidak dipakai sebagai dasar kesimpulan.")

# ---------------------------------------------------------------- Advanced
with tab3:
    st.subheader("Kategori permintaan (Low / Medium / High Demand)")
    st.caption("Manual grouping berbasis kuantil pada jumlah penyewaan per jam; batas kategori dihitung di notebook, bukan machine learning.")
    a, b = st.columns(2)

    dist = fdf["demand_category"].value_counts().reindex(DEMAND).reset_index()
    dist.columns = ["demand_category", "jumlah"]
    fig_d = px.bar(dist, x="demand_category", y="jumlah", color="demand_category", color_discrete_map=DEMAND_COLORS, text="jumlah",
                   labels={"demand_category": "Kategori", "jumlah": "Jumlah baris (jam)"})
    fig_d.update_layout(showlegend=False, title="Distribusi kategori")
    a.plotly_chart(fig_d)

    comp = (pd.crosstab(fdf["season_label"], fdf["demand_category"], normalize="index") * 100).reset_index().melt(
        id_vars="season_label", var_name="Kategori", value_name="Persen")
    fig_c = px.bar(comp, x="season_label", y="Persen", color="Kategori", color_discrete_map=DEMAND_COLORS,
                   category_orders={"Kategori": DEMAND}, labels={"season_label": "Musim", "Persen": "Proporsi baris (%)"})
    fig_c.update_layout(title="Komposisi kategori per musim")
    b.plotly_chart(fig_c)

    prof = fdf.groupby("demand_category", observed=True).agg(
        rata2_suhu_C=("temp_c", "mean"), rata2_kelembapan_pct=("hum_pct", "mean"), rata2_jam=("hr", "mean"), jumlah=("cnt", "size")).round(2)
    st.dataframe(prof, width="stretch")
    st.info("**Insight:** High Demand identik dengan kondisi hangat dan kering serta jam sibuk; Winter didominasi Low Demand, Summer paling banyak High Demand "
            "(angka pada data penuh tertera di notebook).")

# ---------------------------------------------------------------- Validasi harian (data_2.csv)
with tab4:
    st.subheader("Validasi BQ2 pada tingkat harian (data_2.csv)")
    st.caption("Filter yang berlaku: periode, musim, cuaca, dan tipe hari (filter jam tidak berlaku pada data harian).")
    dmask = (
        (daily["dteday"].dt.date >= date_range[0]) & (daily["dteday"].dt.date <= date_range[1])
        & daily["season_label"].isin(sel_seasons) & daily["weather_label"].isin(sel_weathers) & daily["day_type"].isin(sel_days)
    )
    fd = daily[dmask]
    if fd.empty:
        st.warning("Tidak ada data harian untuk kombinasi filter ini.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Jumlah hari", f"{len(fd):,}")
        m2.metric("Rata-rata penyewaan per hari", f"{fd['cnt'].mean():,.0f}")
        m3.metric("Total penyewaan", f"{int(fd['cnt'].sum()):,}")

        c1, c2 = st.columns(2)
        dw = fd.groupby("weather_label", observed=True)["cnt"].agg(rata_rata="mean", hari="count").reset_index()
        dw["weather_label"] = dw["weather_label"].astype(str)
        fig_dw = px.bar(dw, x="weather_label", y="rata_rata", text=dw["rata_rata"].round(0), color="weather_label",
                        color_discrete_map=dict(zip(WEATHERS, ["#2ca02c", "#bcbd22", "#d62728", "#c7c7c7"])),
                        hover_data=["hari"], labels={"weather_label": "Kondisi cuaca", "rata_rata": "Rata-rata penyewaan per hari (unit sepeda)"})
        fig_dw.update_layout(showlegend=False, title="Rata-rata harian per kondisi cuaca")
        c1.plotly_chart(fig_dw)

        mt = fd.groupby(["year", "mnth"])["cnt"].mean().reset_index()
        mt["year"] = mt["year"].astype(str)
        fig_mt = px.line(mt, x="mnth", y="cnt", color="year", markers=True,
                         labels={"mnth": "Bulan", "cnt": "Rata-rata penyewaan per hari (unit sepeda)", "year": "Tahun"})
        fig_mt.update_xaxes(dtick=1)
        fig_mt.update_yaxes(rangemode="tozero")
        fig_mt.update_layout(title="Tren rata-rata harian per bulan")
        c2.plotly_chart(fig_mt)

        base_d = dw.loc[dw["weather_label"] == "Clear/Partly Cloudy", "rata_rata"]
        msgs = []
        if not base_d.empty:
            for w in ["Mist/Cloudy", "Light Rain/Snow"]:
                row = dw.loc[dw["weather_label"] == w, "rata_rata"]
                if not row.empty:
                    msgs.append(f"**{w}** {row.iloc[0]:,.0f} vs cuaca cerah {base_d.iloc[0]:,.0f} penyewaan/hari ({(row.iloc[0] / base_d.iloc[0] - 1) * 100:+.1f}%)")
        st.info("**Insight (sesuai filter):** " + ("; ".join(msgs) if msgs else "sertakan cuaca cerah dan cuaca lain untuk melihat persentase penurunan") + ". "
                "Pada data penuh, arah temuan sama dengan analisis per jam; hanya ada 21 hari Light Rain/Snow, jadi angkanya berbasis sampel kecil.")

st.caption("Sumber data: Fanaee-T & Gama (2013), Bike Sharing Dataset. Dikerjakan oleh M Fahril Luthfi.")
