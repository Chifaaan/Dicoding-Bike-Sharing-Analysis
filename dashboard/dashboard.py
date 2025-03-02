import streamlit as st
import pandas as pd
import warnings
import plotly.express as px
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

#Setting Streamlit
st.set_page_config(
    page_title="Bike ",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="images/bicycle.png")

#Grouping kebutuhan visualisasi
df = pd.read_csv('main_data.csv')
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
tahun_list = ["All year"] + sorted(df["year"].unique().tolist())

monthly_rentals = df.resample("M")[["total", "casual", "registered"]].sum().reset_index()
df["holiday_label"] = df["holiday"].map({0: "Workday", 1: "Holiday"})
holiday_effect = df.groupby("holiday_label")["total"].mean().reset_index()
weather_effect = df.groupby("weathersit")["total"].mean().reset_index()

seasonal_rentals = df.groupby("season")["total"].sum().reset_index()
weekday_rental = df.groupby("weekday")["total"].sum().reset_index()
weekday_rentals = weekday_rental.sort_values(by="total", ascending=False)






with st.sidebar:
    st.title("Dicoding Bike Rental Dashboard")
    st.image('bicycle.png')

    #- Filter Tahun -#
    tahun = st.sidebar.selectbox("Pilih Tahun", tahun_list)
    if tahun != "All year":
        df = df[df["year"] == int(tahun)]
    
    st.write("By Muhammad Nur Irfan   itzirfanmt@gmail.com")
    collink, colgit = st.sidebar.columns(2)

    with collink:
        st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/muhammad-nur-irfan/)")
    with colgit:
        st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/Chifaaan)")
   
st.title("Bike Rental Dashboard")
#Jumlah Sepeda Tersedia & Total User
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Total Penyewaan", df["total"].sum())
col2.metric("Jumlah Registered User", df['registered'].sum())
col3.metric("Jumlah Casual User", df["casual"].sum())

# Perkembangan Penyewaan Tiap Tahun
fig = px.line(
    monthly_rentals,
    x="date",
    y=["total", "casual", "registered"],
    markers=True,
    title="Perkembangan Penyewaan Sepeda per Bulan",
    labels={"date": "Tanggal", "value": "Jumlah Penyewaan"},
)
st.plotly_chart(fig, use_container_width=True)

colpie, colbar = st.columns(2)

with colpie:
    # Visualisasi Pengaruh Hari Libur terhadap Penyewaan Sepeda
    fig_pie_chart = px.pie(
        holiday_effect,
        names="holiday_label",
        values="total",
        color="holiday_label",
    )
    fig_pie_chart.update_traces(textinfo='percent+label', textfont_size=18, marker=dict(line=dict(color='#000000',width=1)))
    st.markdown("#### Pengaruh Hari Libur terhadap Penyewaan Sepeda")
    st.plotly_chart(fig_pie_chart)


    # Visualisasi Pengaruh Cuaca terhadap Penyewaan Sepeda
    fig_pie_chart = px.pie(
    weather_effect,
    names="weathersit",
    values="total",
    color="weathersit"
)
    fig_pie_chart.update_traces(textinfo='percent+label', textfont_size=18, marker=dict(line=dict(color='#000000',width=1)))
    st.markdown("#### Pengaruh Cuaca terhadap Penyewaan Sepeda")
    st.plotly_chart(fig_pie_chart)


with colbar:
    # Visualisasi Persebaran Penyewaan Sepeda Berdasarkan Musim
    fig = px.bar(
        seasonal_rentals,
        x="season",
        y="total",
        color="season",
        labels={"season": "Musim", "total": "Total Penyewaan"},
        text_auto=True
    )
    st.markdown("#### Persebaran Penyewaan Sepeda Berdasarkan Musim")
    st.plotly_chart(fig, use_container_width=True)

    # Visualisasi Ranking Hari Berdasarkan Jumlah Penyewaan Sepeda
    fig = px.bar(
        weekday_rentals,
        x="weekday",
        y="total",
        color="weekday",
        labels={"weekday": "Hari", "total": "Total Penyewaan"},
        text_auto=True
    )
    st.markdown("#### Ranking Hari Berdasarkan Jumlah Penyewaan Sepeda")
    st.plotly_chart(fig, use_container_width=True)


# Fungsi manual clustering berdasarkan total rentals
def manual_clustering(value):
    if value < 1000:
        return "Low Usage"
    elif 1000 <= value <= 3000:
        return "Medium Usage"
    else:
        return "High Usage"

df["usage_cluster"] = df["total"].apply(manual_clustering)

# Kategorisasi suhu menjadi 'Cold', 'Moderate', dan 'Hot'
bins = [df["temp"].min(), 10, 20, df["temp"].max()]
labels = ["Cold", "Moderate", "Hot"]
df["temp_category"] = pd.cut(df["temp"], bins=bins, labels=labels, include_lowest=True)

# Scatter Plot - Manual Clustering berdasarkan Suhu
fig_scatter = px.scatter(
    df,
    x="temp",
    y="total",
    color="usage_cluster",
    labels={"temp": "Temperature", "total": "Total Rentals"},
    opacity=0.7
)

# Bar Chart - Total Penyewaan Berdasarkan Kategori Suhu
temp_rentals = df.groupby("temp_category")["total"].sum().reset_index()

fig_bar = px.bar(
    temp_rentals,
    x="temp_category",
    y="total",
    color="temp_category",
    labels={"temp_category": "Temperature Category", "total": "Total Rentals"},
    text_auto=True
)

# Menampilkan visualisasi di Streamlit
with colpie:
    st.markdown("#### Clustering Manual Berdasarkan Suhu")
    st.plotly_chart(fig_scatter, use_container_width=True)
with colbar:
    st.markdown("#### Total Penyewaan Berdasarkan Kategori Suhu")
    st.plotly_chart(fig_bar, use_container_width=True)
