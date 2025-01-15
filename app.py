import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Thiết lập trang
st.set_page_config(
    page_title="Ứng dụng Demo Streamlit",
    page_icon="📊",
    layout="wide"
)

# Tiêu đề ứng dụng
st.title("📊 Ứng dụng Phân tích Dữ liệu Đơn giản")

# Sidebar
st.sidebar.header("Cài đặt")
uploaded_file = st.sidebar.file_uploader("Tải lên file CSV của bạn", type=['csv'])

# Tạo dữ liệu mẫu nếu không có file được tải lên
if uploaded_file is None:
    # Tạo dữ liệu mẫu
    data = pd.DataFrame({
        'Ngày': pd.date_range(start='2024-01-01', periods=100),
        'Doanh thu': np.random.randint(1000, 5000, 100),
        'Chi phí': np.random.randint(500, 3000, 100),
        'Danh mục': np.random.choice(['A', 'B', 'C'], 100)
    })
else:
    data = pd.read_csv(uploaded_file)

# Main content
st.header("Tổng quan dữ liệu")

# Hiển thị dữ liệu
col1, col2 = st.columns(2)
with col1:
    st.subheader("Dữ liệu thô")
    st.dataframe(data.head())

with col2:
    st.subheader("Thống kê cơ bản")
    st.write(data.describe())

# Vẽ biểu đồ
st.header("Phân tích trực quan")

# Biểu đồ 1
if 'Doanh thu' in data.columns and 'Ngày' in data.columns:
    fig1 = px.line(data, x='Ngày', y='Doanh thu', title='Xu hướng doanh thu theo thời gian')
    st.plotly_chart(fig1)

# Biểu đồ 2
if 'Danh mục' in data.columns and 'Doanh thu' in data.columns:
    fig2 = px.bar(data.groupby('Danh mục')['Doanh thu'].sum().reset_index(), 
                  x='Danh mục', y='Doanh thu', 
                  title='Doanh thu theo danh mục')
    st.plotly_chart(fig2)

# Tính toán và hiển thị các chỉ số KPI
st.header("Chỉ số KPI")
col3, col4, col5 = st.columns(3)

with col3:
    if 'Doanh thu' in data.columns:
        total_revenue = data['Doanh thu'].sum()
        st.metric(label="Tổng doanh thu", value=f"{total_revenue:,.0f} đ")

with col4:
    if 'Chi phí' in data.columns:
        total_cost = data['Chi phí'].sum()
        st.metric(label="Tổng chi phí", value=f"{total_cost:,.0f} đ")

with col5:
    if 'Doanh thu' in data.columns and 'Chi phí' in data.columns:
        profit = total_revenue - total_cost
        st.metric(label="Lợi nhuận", value=f"{profit:,.0f} đ")

# Thêm tương tác với người dùng
st.header("Phân tích tùy chỉnh")
if 'Danh mục' in data.columns:
    selected_category = st.multiselect(
        'Chọn danh mục để phân tích:',
        options=data['Danh mục'].unique(),
        default=data['Danh mục'].unique()[0]
    )
    
    filtered_data = data[data['Danh mục'].isin(selected_category)]
    st.write(filtered_data)

# Footer
st.markdown("---")
st.markdown("Được tạo bằng Streamlit ❤️")
