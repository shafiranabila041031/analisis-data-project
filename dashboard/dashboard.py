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
    st.write("Pilih rentang tanggal untuk mengubah data pada dashboard.")

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
filtered_hour = hour_df[(hour_df["dteday"].dt.date >= start_date) & (hour_df["dteday"].dt.date <= end_date)]


st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard interaktif ini menampilkan analisis penyewaan sepeda. Semua visualisasi di bawah ini akan menyesuaikan dengan rentang waktu yang Anda pilih di *sidebar*.")

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

st.subheader("📈 Tren Penyewaan Sepeda Bulanan")
monthly_trend = filtered_day.groupby(['year', 'month'])['cnt'].sum().reset_index()

if not monthly_trend.empty:
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly_trend, x='month', y='cnt', hue='year', marker='o', palette='Set1', linewidth=2.5, ax=ax1)
    ax1.set_title('Tren Penyewaan Sepeda Bulanan Berdasarkan Filter', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Bulan', fontsize=12)
    ax1.set_ylabel('Total Penyewaan', fontsize=12)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
    st.pyplot(fig1)
else:
    st.info("Data tidak cukup untuk menampilkan tren bulanan pada rentang tanggal ini.")

st.markdown("<br>", unsafe_allow_html=True) # Spasi antar grafik

st.subheader("⏰ Pola Jam Sibuk (Rush Hour) Pada Hari Kerja")
workdays_data = filtered_hour[filtered_hour['workingday'] == 1]

if not workdays_data.empty:
    hourly_trend = workdays_data.groupby('hr')['cnt'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.barplot(data=hourly_trend, x='hr', y='cnt', color='#4C72B0', ax=ax2)
    ax2.set_title('Rata-rata Penyewaan per Jam (Berdasarkan Rentang Waktu Dipilih)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Jam Dalam Sehari (00:00 - 23:00)', fontsize=12)
    ax2.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax2.set_xticks(range(0, 24))
    st.pyplot(fig2)
else:
    st.info("Tidak ada data hari kerja pada rentang tanggal yang dipilih.")

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("👥 Komposisi Tipe Pengguna")
    if total_rentals > 0:
        fig3, ax3 = plt.subplots(figsize=(6, 6))
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
    else:
        st.info("Tidak ada data pengguna.")

with right_col:
    st.subheader("⛅ Pengaruh Cuaca")
    weather_mapping = {
        1: 'Cerah/Berawan',
        2: 'Mendung/Berkabut',
        3: 'Hujan Ringan/Salju',
        4: 'Cuaca Buruk'
    }
    
    weather_avg = filtered_day.groupby('weathersit')['cnt'].mean().reset_index()
    
    if not weather_avg.empty:
        weather_avg['weather_desc'] = weather_avg['weathersit'].map(weather_mapping)
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        sns.barplot(data=weather_avg, x='weather_desc', y='cnt', palette='viridis', ax=ax4)
        ax4.set_title('Rata-rata Penyewaan Berdasarkan Cuaca', fontsize=12, fontweight='bold')
        ax4.set_xlabel('', fontsize=10)
        ax4.set_ylabel('Rata-rata Peminjaman', fontsize=10)
        plt.xticks(rotation=15) # Memiringkan label agar tidak bertumpuk
        
        for p in ax4.patches:
            ax4.annotate(format(p.get_height(), '.0f'), 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha = 'center', va = 'center', 
                         xytext = (0, 9), 
                         textcoords = 'offset points')
        st.pyplot(fig4)
    else:
        st.info("Tidak ada data cuaca.")

st.caption("Bike Sharing Data Analytics Dashboard - Dicoding Submission")
