# analisis-data-project
# submission-proyek-analisis-data

# Bike Sharing Data Analysis Dashboard

## Deskripsi Proyek
Proyek ini merupakan tugas akhir (submission) untuk kelas **Belajar Analisis Data dengan Python** di Dicoding. Proyek ini bertujuan untuk menganalisis dataset *Bike Sharing* guna mendapatkan *insight* bisnis terkait pola pertumbuhan penyewaan dan perilaku komuter. Hasil analisis ini divisualisasikan melalui *dashboard* interaktif menggunakan Streamlit.

## Pertanyaan Bisnis (S.M.A.R.T)
Analisis dalam proyek ini dirancang secara spesifik untuk menjawab dua pertanyaan bisnis berikut:
1. Bagaimana tren pertumbuhan total penyewaan sepeda secara bulanan (*Month-over-Month*) sepanjang tahun 2012 jika dibandingkan dengan tahun 2011, guna merencanakan target penambahan kapasitas armada sepeda di tahun depan?
2. Pada jam berapakah rata-rata volume penyewaan sepeda mencapai puncaknya (*rush hour*) khusus pada hari kerja (*workingday*) selama Kuartal ke-4 (Bulan Oktober - Desember) tahun 2012, agar tim operasional dapat menetapkan jadwal *maintenance* rutin tanpa mengganggu pelanggan?

## Analisis Lanjutan (Advanced Analysis)
Proyek ini mengimplementasikan teknik **Clustering** dengan pendekatan **Manual Binning** (tanpa menggunakan algoritma *Machine Learning*). 
Menggunakan fungsi `pd.qcut()`, performa penyewaan harian dikelompokkan menjadi tiga kategori permintaan:
- **Low Demand**
- **Medium Demand**
- **High Demand**

Hasil analisis lanjutan menunjukkan bahwa kondisi *High Demand* memiliki korelasi yang sangat kuat dengan cuaca yang cerah dan suhu lingkungan yang hangat, sedangkan cuaca buruk terbukti secara instan menekan angka penyewaan ke level *Low Demand*.

## Cara Menjalankan Dashboard (Setup & Run)

### 1. Persiapan Environment
Sangat disarankan untuk menggunakan *virtual environment* agar *library* proyek ini terisolasi dengan baik. Buka terminal/command prompt Anda:

**Menggunakan Venv (Python Bawaan):**
```bash
# Membuat virtual environment bernama "env"
python -m venv env

# Mengaktifkan environment (Untuk pengguna Windows)
env\Scripts\activate

# Mengaktifkan environment (Untuk pengguna Mac/Linux)
source env/bin/activate
