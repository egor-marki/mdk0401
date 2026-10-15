import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Автосалон — Аналитика", page_icon="🚗", layout="wide")
st.title("🚗 Автосалон — Панель руководителя")

# === БОКОВАЯ ПАНЕЛЬ ===
with st.sidebar:
    st.header("⚙️ Фильтры")
    days = st.selectbox("Период", [7, 30, 90, 365], index=1,
                        format_func=lambda x: f"{x} дней")
    if st.button("🔄 Обновить"):
        st.cache_data.clear()
        st.rerun()

# # ФУНКЦИИ ЗАГРУЗКИ ДАННЫХ ИЗ API
@st.cache_data(ttl=60)
def load_kpi(days):
    return requests.get(f"{API_URL}/api/reports/kpi/", params={"days": days}).json()

@st.cache_data(ttl=60)
def load_revenue(days):
    data = requests.get(f"{API_URL}/api/reports/revenue/", params={"days": days}).json()
    return pd.DataFrame(data)

@st.cache_data(ttl=60)
def load_top_models():
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/top-models/").json())

@st.cache_data(ttl=60)
def load_manager_load(days):
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/manager-load/", params={"days": days}).json())

@st.cache_data(ttl=60)
def load_stock():
    return pd.DataFrame(requests.get(f"{API_URL}/api/reports/stock/").json())

# # KPI-ПЛИТКИ
kpi = load_kpi(days)
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Выручка", f"{kpi['revenue']:,.0f} ₽")
c2.metric("📦 Продажи", kpi["sales_count"])
c3.metric("📊 Средний чек", f"{kpi['avg_check']:,.0f} ₽")
c4.metric("🚘 В наличии", kpi["in_stock"])

# # ГРАФИК ВЫРУЧКИ
st.header("📈 Динамика выручки")
revenue_df = load_revenue(days)
if not revenue_df.empty:
    fig = px.line(revenue_df, x="date", y="total", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# # 2 КОЛОНКИ
coll, col2 = st.columns(2)

with coll:
    st.header("🏆 Топ-5 моделей")
    top = load_top_models()
    if not top.empty:
        fig = px.bar(top, x="count", y="model", color="brand", orientation="h")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("👤 Загрузка менеджеров")
    managers = load_manager_load(days)
    if not managers.empty:
        fig = px.pie(managers, values="orders", names="manager")
        st.plotly_chart(fig, use_container_width=True)

# # СКЛАД
st.header("🏢 Состояние склада")
stock = load_stock()
if not stock.empty:
    fig = px.pie(stock, values="count", names="status",
                 color_discrete_map={"available": "green", "reserved": "orange", "sold": "red"})
    st.plotly_chart(fig, use_container_width=True)
