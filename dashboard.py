import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency  # Pastikan modul ini sudah terinstal

# Konfigurasi tampilan Streamlit
st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")

# Coba baca file CSV dengan path yang benar
FILE_PATH = "all_df_cleaned.csv"  # Sesuaikan dengan lokasi file
if os.path.exists(FILE_PATH):
    all_df = pd.read_csv(FILE_PATH)
else:
    st.warning("File tidak ditemukan! Silakan unggah file CSV secara manual.")
    uploaded_file = st.file_uploader("Upload file CSV", type="csv")
    if uploaded_file is not None:
        all_df = pd.read_csv(uploaded_file)
    else:
        st.stop()  # Berhenti jika tidak ada file

# Menampilkan beberapa baris pertama data
st.write("### Data Preview")
st.dataframe(all_df.head())

# Contoh visualisasi sederhana
st.write("### Visualisasi Data")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(all_df['harga'], bins=30, kde=True, ax=ax)
ax.set_title("Distribusi Harga Produk")
st.pyplot(fig)
