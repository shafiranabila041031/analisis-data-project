import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)
    
    day_path = os.path.join(BASE_DIR, "final_cleaned_day.csv")
    hour_path = os.path.join(BASE_DIR, "final_cleaned_hour.csv")
    
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)
    
    # Memastikan format datetime
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    day_df['year'] = day_df['dteday'].dt.year
    day_df['month'] = day_df['dteday'].dt.month
    hour_df['year'] = hour_df['dteday'].dt.year
    hour_df['month'] = hour_df['dteday'].dt.month
    
    return day_df, hour_df

day_df, hour_df = load_data()


with st.sidebar:
    st.header("🚲 Filter Data")
    st.write("Pilih rentang tanggal untuk melihat ringkasan metrik di bawah.")

    min_date = day_df["dteday"].min().date()
    max_date = day_df["dteday"].max().date()

    date_range = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Memfilter data harian berdasarkan input tanggal di sidebar
filtered_day = day_df[(day_df["dteday"].dt.date >= start_date) & (day_df["dteday"].dt.date <= end_date)]


st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard ini menyajikan hasil analisis data historis penyewaan sepeda berdasarkan kerangka pertanyaan bisnis **S.M.A.R.T**.")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_day['cnt'].sum()
    st.metric("Total Peminjaman (Terfilter)", value=f"{total_rentals:,}")
with col2:
    total_registered = filtered_day['registered'].sum()
    st.metric("Pengguna Registered (Terfilter)", value=f"{total_registered:,}")
with col3:
    total_casual = filtered_day['casual'].sum()
    st.metric("Pengguna Casual (Terfilter)", value=f"{total_casual:,}")

st.divider()

tab1, tab2 = st.tabs(["📈 Pertanyaan 1: Tren MoM (2011 vs 2012)", "⏰ Pertanyaan 2: Rush Hour Q4 2012"])


with tab1:
    st.subheader("Tren Pertumbuhan Penyewaan Sepeda Bulanan")
    st.markdown("**Pertanyaan Bisnis:** *Bagaimana tren pertumbuhan total penyewaan sepeda secara bulanan (Month-over-Month) sepanjang tahun 2012 jika dibandingkan dengan tahun 2011, guna merencanakan target penambahan kapasitas armada sepeda di tahun depan?*")
    
    # Agregasi data
    monthly_trend = day_df.groupby(['year', 'month'])['cnt'].sum().reset_index()
    
    # Visualisasi
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly_trend, x='month', y='cnt', hue='year', marker='o', palette='Set1', linewidth=2.5, ax=ax1)
    ax1.set_title('Perbandingan Tren Bulanan (2011 vs 2012)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Bulan', fontsize=12)
    ax1.set_ylabel('Total Penyewaan', fontsize=12)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
    st.pyplot(fig1)
    
    # Insight dan Rekomendasi
    with st.expander("💡 Lihat Kesimpulan & Rekomendasi (Action Item)"):
        st.write("**Kesimpulan:** Bisnis mengalami pertumbuhan (*growth*) Year-over-Year (YoY) yang sangat konsisten. Grafik juga menunjukkan sifat musiman (*seasonal*) yang kuat, di mana puncak permintaan selalu terjadi pada bulan Agustus-September, lalu menurun di akhir tahun.")
        st.write("**Rekomendasi:** Manajemen harus menyelesaikan pengadaan armada sepeda baru untuk tahun 2013 paling lambat pada bulan **April/Mei** agar siap menghadapi lonjakan permintaan di kuartal ketiga.")


with tab2:
    st.subheader("Pola Jam Sibuk (Rush Hour) Hari Kerja di Kuartal 4 (2012)")
    st.markdown("**Pertanyaan Bisnis:** *Pada jam berapakah rata-rata volume penyewaan sepeda mencapai puncaknya (rush hour) khusus pada hari kerja (workingday) selama Kuartal ke-4 (Bulan Oktober - Desember) tahun 2012, agar tim operasional dapat menetapkan jadwal maintenance rutin tanpa mengganggu pelanggan?*")
    
    q4_2012_workdays = hour_df[(hour_df['year'] == 2012) & 
                               (hour_df['month'].isin([10, 11, 12])) & 
                               (hour_df['day_type'] == 'Hari Kerja')] 
    
    if q4_2012_workdays.empty:
         q4_2012_workdays = hour_df[(hour_df['year'] == 2012) & 
                               (hour_df['month'].isin([10, 11, 12])) & 
                               (hour_df['workingday'] == 1)]

    hourly_q4 = q4_2012_workdays.groupby('hr')['cnt'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=hourly_q4, x='hr', y='cnt', color='#4C72B0', ax=ax2)
    ax2.set_title('Rata-rata Penyewaan per Jam (Hari Kerja - Q4 2012)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Jam Dalam Sehari (00:00 - 23:00)', fontsize=12)
    ax2.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax2.set_xticks(range(0, 24))
    st.pyplot(fig2)
    
    with st.expander("💡 Lihat Kesimpulan & Rekomendasi (Action Item)"):
        st.write("**Kesimpulan:** Pada hari kerja, terdapat dua puncak ekstrem (*rush hour*) yaitu pada pukul **08:00 pagi** dan pukul **17:00-18:00 sore**. Ini mengonfirmasi bahwa penyewa dominan adalah segmen komuter/pekerja. Jam dengan aktivitas terendah berada di rentang 00:00 hingga 05:00.")
        st.write("**Rekomendasi:** Tim teknisi wajib memindahkan seluruh jadwal perbaikan rutin (maintenance) ke 'jam lembah' (pukul **22:00 - 05:00 pagi**). Dilarang keras melakukan penarikan unit sepeda rusak pada jam-jam sibuk pagi dan sore hari agar operasional tidak terganggu.")

st.caption("Bike Sharing Data Analytics Dashboard - Created for Dicoding Submission")
