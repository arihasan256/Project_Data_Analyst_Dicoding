import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

##Karena keterbatasan waktu pertanyaan 5 dan 6 tidak dikembangkan dalam streamlit

# Mempersiapkan data
df_day = pd.read_csv("dataset/day.csv", delimiter=",")
df_hour = pd.read_csv("dataset/hour.csv", delimiter=",")
df_day.head()
sns.set(style='dark')

# Mengubah tipe data menjadi datetime
datetime_columns = ["dteday"]
for column in datetime_columns:
    df_day[column] = pd.to_datetime(df_day[column])
    df_hour[column] = pd.to_datetime(df_hour[column])

#Mengubah keterangan pada data integer menggunakan fungsi map
def map_year(df):
    df["yr"] = df["yr"].map({0: 2011, 1: 2012})
    return df

df_day = map_year(df_day)
df_hour = map_year(df_hour) 

def map_season(df):
    df["season"] = df["season"].map({1:"Spring", 2:"Summer", 3:"Fall", 4:"Winter"})
    return df

df_day = map_season(df_day)
df_hour = map_season(df_hour)

def map_weekdays(df):
    df["weekday"] = df["weekday"].map({0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6: "Saturday"})
    return df

df_day = map_weekdays(df_day)
df_hour = map_weekdays(df_hour)

def map_mnth(df):
    df["mnth"] = df["mnth"].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    })
    return df

df_day = map_mnth(df_day)
df_hour = map_mnth(df_hour)

def map_weather(df):
    df["weathersit"] = df["weathersit"].map({
    1: 'Clear',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Tunderstorm/Fog Snow'
    })
    return df

df_day = map_weather(df_day)
df_hour = map_weather(df_hour)


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='mnth').agg({
        'cnt': 'sum'
    })
    ordered_months = [
        'January','February','March','April','May','June','July',
        'August','September','October','November','December'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'cnt': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'cnt': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'cnt': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    })
    return weather_rent_df

# Membuat komponen filter
min_date = pd.to_datetime(df_day['dteday']).dt.date.min()
max_date = pd.to_datetime(df_day['dteday']).dt.date.max()
 
## STREAMLIT EXPLORATION

#slidebar
with st.sidebar:
    # Company Name
    st.image("img_bangkit.jpg")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Calendar',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_day[(df_day['dteday'] >= str(start_date)) & 
                (df_day['dteday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat judul
st.header('Bike Sharing Data Analysis Dashboard 📊🚲')

## 1
st.caption ("""Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return 
back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return 
back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of 
over 500 thousands bicycles. Today, there exists great interest in these systems due to their important role in traffic, 
environmental and health issues. 

Apart from interesting real world applications of bike sharing systems, the characteristics of data being generated by
these systems make them attractive for the research. Opposed to other transport services such as bus or subway, the duration
of travel, departure and arrival position is explicitly recorded in these systems. This feature turns bike sharing system into
a virtual sensor network that can be used for sensing mobility in the city. Hence, it is expected that most of important
events in the city could be detected via monitoring these data.""")

st.caption ("created and visualize by Ari Hasan")

## Pertanyaan 1
st.subheader('1. Tren dalam Peminjaman Sepeda pada tahun 2011 dan 2012')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['cnt'],
    marker='o', 
    linewidth=2,
    color='#5F5D9C'
)

for index, row in enumerate(monthly_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)
st.caption("Terdapat perubahan signifikan jumlah user penyewa sepeda dari tahun 2011 sampai 2012, terlihat jumlah user pada tahun 2012 lebih banyak daripada tahun sebelumnya, hal ini menandakan bisnis berkembang dengan baik.\nSelain itu pada grafik terlihat tren jumlah user tiap bulannya, telihat bahwa terjadi tren naik pada  bylan januari sampai bulan september pada tahun 2012 dan selanjutnya terjadi penurunan dari bulan september samapi desermber, pola tersebut mirip dengan tahun 2011")


## Pertanyaan 2
st.subheader('2. Jumlah User Penyewa Sepeda Ditinjau dari Musim')

fig, ax = plt.subplots(figsize=(16, 8))
warna_register = "#A4CE95"
warna_casual = "#6196A6"

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color=warna_register,
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color=warna_casual,
    ax=ax
)
for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)
st.caption("Pada grafik terlihat bahwa pada saat musim gugur (fall) merupakan musim dimana penyewa sepeda terbanyak dari musim lainnya.\nDapat kita lihat pula perbadingan antara pengguna casual dan pengguna registered pada tiap musim, terlihat bahwa pengguna registered lebih banyak daripada pengguna casual, hal ini merupakan kabar yang baik bagi perusahaan.")

## Pertanyaan 3
st.subheader('3. Pengaruh Kondisi Cuaca Terhadap Jumlah Rental')
fig, ax = plt.subplots(figsize=(16, 8))
warna = ["#5F5D9C", "#6196A6", "#A4CE95", "#F4EDCC"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['cnt'],
    palette=warna,
    ax=ax
)

for index, row in enumerate(weather_rent_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)
st.caption("Kondisi cuaca sangat mempengaruhi jumlah penyewa sepeda, seperti pada grafik saat cuaca cerah atau sedikit berawan jumlah penyewa lebih banyak daripada saat cuaca hujan atau badai petir")

## Pertanyaan 4
st.subheader('4. Pengaruh Temperature Terhadap Jumlah Rental Sepeda')
fig, ax = plt.subplots(figsize=(14, 6))
warna = "#5F5D9C"

sns.scatterplot(
    x='temp',
    y='cnt',
    data=main_df, 
    alpha=0.7,
    color=warna
)

ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)
plt.xlabel('Temperature', fontsize=14)
plt.ylabel('Count', fontsize=14)
st.pyplot(fig)
st.caption("Pada scatterplot tersebut terlihat bahwa temperature turut mempengaruhi jumlah penyewa sepeda, jumlah penyewa sepeda akan banyak saat temperature normal (kisaran 25 - 30 derajat)")

