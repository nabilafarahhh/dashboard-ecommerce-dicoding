import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

# LOAD DATA
df = pd.read_csv('dashboard/main_data.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

st.sidebar.header("🔍 Filter Tanggal")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

df = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

# HEADER
st.title('📊 E-Commerce Sales Dashboard')
st.caption('Analisis performa penjualan dan kategori produk')

# METRICS
total_revenue = df['price'].sum()
total_orders = df['order_id'].nunique()
total_products = df['product_id'].nunique()
avg_price = df['price'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Orders", total_orders)
col3.metric("🛒 Produk", total_products)
col4.metric("💸 Avg Price", f"${avg_price:,.2f}")

# DATA PREPARATION
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

monthly_revenue = df.groupby('order_month')['price'].sum().reset_index()
monthly_revenue = monthly_revenue.sort_values(by='order_month')

category_sales = df.groupby('product_category_name_english')['product_id'].count().reset_index()
category_sales = category_sales.rename(columns={'product_id': 'total_sales'})
category_sales = category_sales.sort_values(by='total_sales', ascending=False).head(10)

# VISUALIZATION
st.markdown("---")

# 📈 Revenue Trend
st.subheader(f'📈 Revenue Bulanan ({start_date} - {end_date})')
fig, ax = plt.subplots()
ax.plot(monthly_revenue['order_month'], monthly_revenue['price'], marker='o')
ax.set_xlabel('Bulan')
ax.set_ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# 🏆 Top Category
st.subheader(f'🏆 Top 10 Kategori Produk ({start_date} - {end_date})')
fig2, ax2 = plt.subplots()
sns.barplot(
    x='total_sales',
    y='product_category_name_english',
    data=category_sales,
    ax=ax2
)
ax2.set_xlabel('Jumlah Penjualan')
ax2.set_ylabel('Kategori')
plt.tight_layout()
st.pyplot(fig2)

# DISTRIBUTION CHART
st.markdown("---")
st.subheader('📊 Distribusi Harga Produk')

fig3, ax3 = plt.subplots()
sns.histplot(df['price'], bins=30, ax=ax3)
ax3.set_xlabel('Harga')
ax3.set_ylabel('Frekuensi')
plt.tight_layout()

st.pyplot(fig3)