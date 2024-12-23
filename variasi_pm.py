# -*- coding: utf-8 -*-
"""Variasi PM

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nhZmvpd0H85Vao9P3ys31oIfBVNzzuxu
"""

# Instalasi pustaka yang diperlukan
!pip install pandas matplotlib openpyxl

# Import pustaka yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt

# Memuat file Excel
file_path = '/content/drive/MyDrive/DATA REVISI/BundaranHI2020-2022.xlsx'  # Sesuaikan path ke lokasi file Anda
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Menampilkan beberapa baris pertama untuk memahami struktur data
print(data.head())

# Konversi kolom 'Tanggal' ke format datetime
data['Tanggal'] = pd.to_datetime(data['Tanggal'])

# Filter data untuk tahun 2020 dan 2021
data_filtered = data[(data['Tanggal'] >= '2020-01-01') & (data['Tanggal'] <= '2021-12-31')]

# Memeriksa nilai non-numerik dalam kolom PM10 dan PM2.5
non_numeric_pm10 = data_filtered['PM10'].apply(lambda x: not pd.api.types.is_number(x))
non_numeric_pm25 = data_filtered['PM2.5'].apply(lambda x: not pd.api.types.is_number(x))

# Menampilkan baris dengan nilai non-numerik
non_numeric_rows = data_filtered[non_numeric_pm10 | non_numeric_pm25]
print(non_numeric_rows)

# Mengganti nilai non-numerik dengan NaN dan melakukan forward-fill untuk menangani data yang hilang
data_filtered['PM10'] = pd.to_numeric(data_filtered['PM10'], errors='coerce')
data_filtered['PM2.5'] = pd.to_numeric(data_filtered['PM2.5'], errors='coerce')

data_filtered['PM10'].fillna(method='ffill', inplace=True)
data_filtered['PM2.5'].fillna(method='ffill', inplace=True)

# Membuat plot data
plt.figure(figsize=(14, 7))
plt.plot(data_filtered['Tanggal'], data_filtered['PM10'], label='PM10', color='blue', alpha=0.5)
plt.plot(data_filtered['Tanggal'], data_filtered['PM2.5'], label='PM2.5', color='cyan', alpha=0.5)
plt.xlabel('Tanggal')
plt.ylabel('Konsentrasi (µg/m³)')
plt.ylim(0, 140)  # Menetapkan skala sumbu y dari 0 hingga 140
plt.legend(fontsize=20)  # Menyesuaikan ukuran font pada legenda
plt.xticks(rotation=45)
plt.tight_layout()

# Menampilkan plot
plt.show()