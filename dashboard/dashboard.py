import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

# Load data
df = pd.read_csv('dashboard/main_data.csv')

# Convert datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# header
st.title('📊 E-Commerce Sales Dashboard')
st.caption('Analisis performa penjualan dan kategori produk')

# METRICS
total_revenue = df['price'].sum()
total_orders = df['order_id'].nunique()
total_products = df['product_id'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("🛒 Total Produk", total_products)

# DATA PREPARATION
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

monthly_revenue = df.groupby('order_month')['price'].sum().reset_index()

category_sales = df.groupby('product_category_name_english')['order_item_id'].count().reset_index()
category_sales = category_sales.sort_values(by='order_item_id', ascending=False).head(10)

# VISUALIZATION
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader('📈 Tren Revenue Bulanan')
    fig, ax = plt.subplots()
    ax.plot(monthly_revenue['order_month'], monthly_revenue['price'], marker='o')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Revenue')
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader('🏆 Top 10 Kategori Produk')
    fig2, ax2 = plt.subplots()
    sns.barplot(
        x='order_item_id',
        y='product_category_name_english',
        data=category_sales,
        ax=ax2
    )
    ax2.set_xlabel('Jumlah Penjualan')
    ax2.set_ylabel('Kategori')
    st.pyplot(fig2)

# INSIGHT
st.markdown("---")
st.subheader("📌 Insight")

top_category = category_sales.iloc[0]['product_category_name_english']

st.write(f"""
- Revenue menunjukkan fluktuasi dari waktu ke waktu yang mencerminkan dinamika penjualan.
- Kategori produk paling populer adalah **{top_category}**, dengan jumlah transaksi tertinggi.
- Hal ini menunjukkan adanya preferensi pelanggan terhadap kategori tertentu.
""")