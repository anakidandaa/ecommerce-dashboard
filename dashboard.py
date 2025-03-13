import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set tema seaborn
sns.set(style='dark')

# Fungsi untuk memuat data
def load_data():
    FILE_PATH = "all_df_cleaned.csv"
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        st.warning("File tidak ditemukan! Silakan unggah file CSV secara manual.")
        uploaded_file = st.file_uploader("Upload file CSV", type="csv")
        if uploaded_file is not None:
            return pd.read_csv(uploaded_file)
        else:
            st.stop()

# Load data
all_df = load_data()

# Konversi kolom datetime
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# Sidebar untuk filter tanggal
with st.sidebar:
    try:
        st.image("https://github.com/anakidandaa/ecommerce-dashboard/blob/main/logo-Photoroom.png")
    except:
        st.write("Logo tidak tersedia.")

    min_date = all_df["order_purchase_timestamp"].min().date()
    max_date = all_df["order_purchase_timestamp"].max().date()

    date_range = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

    # Validasi input tanggal
    if len(date_range) != 2:
        st.error("Silakan pilih rentang waktu yang lengkap (mulai dan akhir).")
        st.stop()
    else:
        start_date, end_date = date_range

# Filter data berdasarkan tanggal
main_df = all_df[
    (all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
].copy()  # Menggunakan `.copy()` untuk menghindari warning

# Dashboard Title
st.header('Dicoding Collection Dashboard :sparkles:')

# Produk Terlaris & Tidak Laku
st.subheader("Produk Terlaris & Tidak Laku")
sum_order_items_df = main_df.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), ax=ax[0], color="blue")
ax[0].set_title("Top 5 Produk Terlaris")

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.tail(5), ax=ax[1], color="red")
ax[1].set_title("Bottom 5 Produk Paling Tidak Laku")

st.pyplot(fig)

# Wilayah dengan Customer Terbanyak
st.subheader("Wilayah dengan Customer Terbanyak")
customer_by_state = main_df.groupby("customer_state")["customer_unique_id"].nunique().reset_index()
customer_by_state = customer_by_state.sort_values(by="customer_unique_id", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="customer_state", y="customer_unique_id", data=customer_by_state.head(10), palette="coolwarm")
ax.set_title("Top 10 Wilayah dengan Customer Terbanyak")
ax.set_xlabel("State")
ax.set_ylabel("Jumlah Customer")

st.pyplot(fig)

# Tren Order Tahunan
st.subheader("Tren Order dalam Beberapa Tahun Terakhir")
main_df["year"] = main_df["order_purchase_timestamp"].dt.year  # Pastikan tanpa warning
order_trend = main_df.groupby("year")["order_id"].count().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="year", y="order_id", data=order_trend, marker="o", color="green")
ax.set_title("Tren Order dari Tahun ke Tahun")
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Order")

st.pyplot(fig)

# Footer
st.caption('Copyright © anakidanda 2025')
