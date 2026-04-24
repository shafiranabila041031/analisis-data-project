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

filtered_day = day_df[(day_df["dteday"].dt.date >= start_date) & (day_df["dteday"].dt.date <= end_date)]

st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard ini menyajikan hasil analisis data historis penyewaan sepeda berdasarkan kerangka pertanyaan bisnis **S.M.A.R.T** serta gambaran umum operasional.")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_day['cnt'].sum()
    st.metric("Total Peminjaman", value=f"{total_rentals:,}")
with col2:
    total_registered = filtered_day['registered'].sum()
    st.metric("Pengguna Registered", value=f"{total_registered:,}")
with col3:
    total_casual = filtered_day['casual'].sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren MoM (Pertanyaan 1)", 
    "⏰ Rush Hour Q4 (Pertanyaan 2)",
    "👥 Proporsi Pengguna",
    "⛅ Pengaruh Cuaca"
])

with tab1:
    st.subheader("Tren Pertumbuhan Penyewaan Sepeda Bulanan")
    st.markdown("**Pertanyaan Bisnis:** *Bagaimana tren pertumbuhan total penyewaan sepeda secara bulanan (Month-over-Month) sepanjang tahun 2012 jika dibandingkan dengan tahun 2011?*")
    
    monthly_trend = day_df.groupby(['year', 'month'])['cnt'].sum().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly_trend, x='month', y='cnt', hue='year', marker='o', palette='Set1', linewidth=2.5, ax=ax1)
    ax1.set_title('Perbandingan Tren Bulanan (2011 vs 2012)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Bulan', fontsize=12)
    ax1.set_ylabel('Total Penyewaan', fontsize=12)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
    st.pyplot(fig1)
    
    with st.expander("💡 Lihat Kesimpulan & Rekomendasi (Action Item)"):
        st.write("**Kesimpulan:** Bisnis mengalami pertumbuhan (*growth*) Year-over-Year (YoY) yang konsisten. Grafik juga menunjukkan sifat musiman (*seasonal*) yang kuat (puncak di Agustus-September).")
        st.write("**Rekomendasi:** Manajemen harus menyelesaikan pengadaan armada sepeda baru untuk tahun 2013 paling lambat pada bulan **April/Mei**.")

with tab2:
    st.subheader("Pola Jam Sibuk (Rush Hour) Hari Kerja di Kuartal 4 (2012)")
    st.markdown("**Pertanyaan Bisnis:** *Pada jam berapakah rata-rata volume penyewaan sepeda mencapai puncaknya khusus pada hari kerja selama Kuartal ke-4 tahun 2012?*")
    
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
        st.write("**Kesimpulan:** Terdapat dua puncak ekstrem (*rush hour*) yaitu pada pukul **08:00 pagi** dan **17:00-18:00 sore**. Jam aktivitas terendah berada di rentang 00:00 hingga 05:00.")
        st.write("**Rekomendasi:** Jadwal perbaikan rutin (maintenance) wajib dipindah ke pukul **22:00 - 05:00 pagi**.")

with tab3:
    st.subheader("Komparasi Tipe Pengguna")
    st.markdown("Visualisasi ini bersifat dinamis mengikuti filter tanggal di *sidebar*.")
    
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    labels = ['Registered', 'Casual']
    sizes = [total_registered, total_casual]
    colors = ['#66b3ff', '#ff9999']
    
    explode = (0.05, 0)
    
    ax3.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 12})
    
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig3.gca().add_artist(centre_circle)
    
    ax3.axis('equal')  
    st.pyplot(fig3)

with tab4:
    st.subheader("Dampak Kondisi Cuaca terhadap Volume Penyewaan")
    st.markdown("Menampilkan rata-rata penyewaan per hari berdasarkan kondisi cuaca (Dinamis sesuai filter).")
    
    weather_mapping = {
        1: 'Cerah / Sebagian Berawan',
        2: 'Mendung / Berkabut',
        3: 'Hujan Ringan / Salju',
        4: 'Cuaca Buruk Ekstrem'
    }
    
    weather_avg = filtered_day.groupby('weathersit')['cnt'].mean().reset_index()
    weather_avg['weather_desc'] = weather_avg['weathersit'].map(weather_mapping)
    
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=weather_avg, x='weather_desc', y='cnt', palette='viridis', ax=ax4)
    ax4.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax4.set_ylabel('Rata-rata Peminjaman', fontsize=12)

    for p in ax4.patches:
        ax4.annotate(format(p.get_height(), '.0f'), 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha = 'center', va = 'center', 
                     xytext = (0, 9), 
                     textcoords = 'offset points')
                     
    st.pyplot(fig4)

st.caption("Bike Sharing Data Analytics Dashboard")
