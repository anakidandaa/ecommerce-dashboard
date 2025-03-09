import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
import urllib

# Load data
@st.cache_data
def load_data():
    all_df = pd.read_csv("all_df_cleaned.csv")
    return all_df

df = load_data()

st.title("Dashboard Analisis E-Commerce")

# Produk Terlaris & Tidak Laku
st.subheader("Produk Terlaris & Tidak Laku")
sum_order_items_df = df.groupby("product_category_name_english")["product_id"].count().reset_index()
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
customer_by_state = df.groupby("customer_state")["customer_unique_id"].nunique().reset_index()
customer_by_state = customer_by_state.sort_values(by="customer_unique_id", ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="customer_state", y="customer_unique_id", data=customer_by_state.head(10), palette="coolwarm")
ax.set_title("Top 10 Wilayah dengan Customer Terbanyak")
ax.set_xlabel("State")
ax.set_ylabel("Jumlah Customer")

st.pyplot(fig)

# Tren Order Tahunan
st.subheader("Tren Order dalam Beberapa Tahun Terakhir")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["year"] = df["order_purchase_timestamp"].dt.year
order_trend = df.groupby("year")["order_id"].count().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="year", y="order_id", data=order_trend, marker="o", color="green")
ax.set_title("Tren Order dari Tahun ke Tahun")
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Order")

st.pyplot(fig)

