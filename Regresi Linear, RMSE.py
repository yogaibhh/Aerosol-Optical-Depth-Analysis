# -*- coding: utf-8 -*-
"""SCR new.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hcc4lSip4b2J4qQYIkWJ4OYdwPTEPsRV
"""

# Install required libraries (jika diperlukan)
!pip install pandas scipy matplotlib
!pip install statsmodels
!pip install sklearn.metrics

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'
pm10_data_path = '/content/drive/MyDrive/DATA SKRIPSI PALING FIXXXXAX/BundaranHI2020-2022.xlsx'

aeronet_data = pd.read_excel(aeronet_data_path)
pm10_data = pd.read_excel(pm10_data_path)

# Ensure both date columns are in datetime format
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'])
pm10_data['Tanggal'] = pd.to_datetime(pm10_data['Tanggal'])

# Filter data for the years 2020 and 2021
aeronet_2020_2021 = aeronet_data[(aeronet_data['Date'].dt.year == 2020) | (aeronet_data['Date'].dt.year == 2021)]
pm10_2020_2021 = pm10_data[(pm10_data['Tanggal'].dt.year == 2020) | (pm10_data['Tanggal'].dt.year == 2021)]

# Aggregate data by month, selecting only numeric columns
numeric_cols_aeronet = aeronet_2020_2021.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols_pm10 = pm10_2020_2021.select_dtypes(include=[np.number]).columns.tolist()

aeronet_monthly = aeronet_2020_2021.groupby(aeronet_2020_2021['Date'].dt.to_period("M"))[numeric_cols_aeronet].mean().reset_index()
pm10_monthly = pm10_2020_2021.groupby(pm10_2020_2021['Tanggal'].dt.to_period("M"))[numeric_cols_pm10].mean().reset_index()

# Rename the date columns for a consistent merge
pm10_monthly.rename(columns={"Tanggal": "Date"}, inplace=True)
aeronet_monthly['Date'] = aeronet_monthly['Date'].dt.to_timestamp()  # Converting Period to Timestamp
pm10_monthly['Date'] = pm10_monthly['Date'].dt.to_timestamp()

# Merge the datasets based on the Date column
merged_monthly_data = pd.merge(aeronet_monthly, pm10_monthly, on="Date")

# Perform linear regression for the combined 2020-2021 data with AOD as X and PM10 as Y
slope, intercept, r_value, p_value, std_err = stats.linregress(merged_monthly_data['AOD_500nm'], merged_monthly_data['PM10'])
r_squared = r_value ** 2

# Prepare values for the plot
x_values = np.linspace(merged_monthly_data['AOD_500nm'].min(), merged_monthly_data['AOD_500nm'].max(), 100)
y_values = slope * x_values + intercept

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(merged_monthly_data['AOD_500nm'], merged_monthly_data['PM10'], color='blue', label='Data Aktual')
plt.plot(x_values, y_values, color='red', label='Garis Regresi')
plt.xlabel('AOD 500nm')
plt.ylabel('PM10 (μg/m³)')
plt.legend()
plt.annotate(annotation_text, xy=(1, 0.5), xycoords='axes fraction', xytext=(10, 0), textcoords='offset points', fontsize=12, ha='left', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))
plt.subplots_adjust(right=0.8)
plt.show()

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'  # Replace with your actual file path
environmental_data_path = '/content/drive/MyDrive/Skripci/BundaranHI2020-2022.xlsx'  # Replace with your actual file path

# Read the data from Excel files
aeronet_data = pd.read_excel(aeronet_data_path)
environmental_data = pd.read_excel(environmental_data_path)

# Convert 'PM10' to numeric and handle non-numeric entries
environmental_data['PM10'] = pd.to_numeric(environmental_data['PM10'], errors='coerce')

# Filter both datasets for the year 2020
aeronet_2020 = aeronet_data[aeronet_data['Date'].dt.year == 2021]
environmental_2020 = environmental_data[environmental_data['Tanggal'].dt.year == 2021]

# Specify the months explicitly
months = [3, 4, 5, 6, 7, 8, 9, 10]  # March to October

# Filter data to include only the specified months
aeronet_2020 = aeronet_2020[aeronet_2020['Date'].dt.month.isin(months)]
environmental_2020 = environmental_2020[environmental_2020['Tanggal'].dt.month.isin(months)]

# Rename columns for consistency and merge datasets on 'Date'
environmental_2020_renamed = environmental_2020.rename(columns={"Tanggal": "Date"})
merged_data_2020 = pd.merge(aeronet_2020, environmental_2020_renamed, on='Date')

# Drop rows with any NaN values in 'AOD_500nm' or 'PM10'
merged_data_2020.dropna(subset=['AOD_500nm', 'PM10'], inplace=True)

# Perform linear regression with AOD as independent variable (X) and PM10 as dependent variable (Y)
slope, intercept, r_value, p_value, std_err = stats.linregress(merged_data_2020['AOD_500nm'], merged_data_2020['PM10'])

# Prepare regression line data
x_values = np.linspace(merged_data_2020['AOD_500nm'].min(), merged_data_2020['AOD_500nm'].max(), 100)
y_values = slope * x_values + intercept

# Creating the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(merged_data_2020['AOD_500nm'], merged_data_2020['PM10'], color='blue', label='Data Aktual')
plt.plot(x_values, y_values, color='red', label='Garis Regresi')

# Annotating the plot with the regression equation, R^2, P-value, and RMSE
annotation_text = f'y = {slope:.4f}x + {intercept:.4f}\n$R^2$ = {r_value**2:.4f}\n$p$-value = {p_value:.3e}\nRMSE = {rmse:.3f}'
plt.annotate(annotation_text, xy=(1, 0.5), xycoords='axes fraction', textcoords='offset points',
             fontsize=12, ha='left', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))


# Adjust margins to accommodate the annotation
plt.subplots_adjust(right=0.8)

# Setting the labels and title
plt.xlabel('AOD 500nm')
plt.ylabel('PM10 (μg/m³)')
plt.legend()
plt.show()

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'
pm10_data_path = '/content/drive/MyDrive/DATA SKRIPSI PALING FIXXXXAX/BundaranHI2020-2022.xlsx'

aeronet_data = pd.read_excel(aeronet_data_path)
pm10_data = pd.read_excel(pm10_data_path)

# Ensure both date columns are in datetime format
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'])
pm10_data['Tanggal'] = pd.to_datetime(pm10_data['Tanggal'])

# Filter data for the years 2020 and 2021
aeronet_2020_2021 = aeronet_data[(aeronet_data['Date'].dt.year == 2020) | (aeronet_data['Date'].dt.year == 2021)]
pm10_2020_2021 = pm10_data[(pm10_data['Tanggal'].dt.year == 2020) | (pm10_data['Tanggal'].dt.year == 2021)]

# Aggregate data by month, selecting only numeric columns
numeric_cols_aeronet = aeronet_2020_2021.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols_pm10 = pm10_2020_2021.select_dtypes(include=[np.number]).columns.tolist()

aeronet_monthly = aeronet_2020_2021.groupby(aeronet_2020_2021['Date'].dt.to_period("M"))[numeric_cols_aeronet].mean().reset_index()
pm10_monthly = pm10_2020_2021.groupby(pm10_2020_2021['Tanggal'].dt.to_period("M"))[numeric_cols_pm10].mean().reset_index()

# Rename the date columns for a consistent merge
pm10_monthly.rename(columns={"Tanggal": "Date"}, inplace=True)
aeronet_monthly['Date'] = aeronet_monthly['Date'].dt.to_timestamp()  # Converting Period to Timestamp
pm10_monthly['Date'] = pm10_monthly['Date'].dt.to_timestamp()

# Merge the datasets based on the Date column
merged_monthly_data = pd.merge(pm10_monthly, aeronet_monthly, on="Date")

# Perform linear regression for the combined 2020-2021 data with PM10 as X and AOD as Y
slope, intercept, r_value, p_value, std_err = stats.linregress(merged_monthly_data['PM10'], merged_monthly_data['AOD_500nm'])
r_squared = r_value ** 2

# Prepare values for the plot
x_values = np.linspace(merged_monthly_data['PM10'].min(), merged_monthly_data['PM10'].max(), 100)
y_values = slope * x_values + intercept

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(merged_monthly_data['PM10'], merged_monthly_data['AOD_500nm'], color='blue', label='Data Aktual')
plt.plot(x_values, y_values, color='red', label='Garis Regresi')
plt.xlabel('PM10 (μg/m³)')
plt.ylabel('AOD 500nm')
plt.legend()

# Annotating the plot with the regression equation, R^2, P-value, and RMSE
annotation_text = f'y = {slope:.4f}x + {intercept:.4f}\n$R^2$ = {r_value**2:.4f}\n$p$-value = {p_value:.3e}\nRMSE = {rmse:.3f}'
plt.annotate(annotation_text, xy=(1, 0.5), xycoords='axes fraction', textcoords='offset points',
             fontsize=12, ha='left', va='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
plt.subplots_adjust(right=0.8)
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'
pm_data_path = '/content/drive/MyDrive/DATA SKRIPSI PALING FIXXXXAX/BundaranHI2020-2022.xlsx'

# Read the data from Excel files
aeronet_data = pd.read_excel(aeronet_data_path)
pm_data = pd.read_excel(pm_data_path)

# Convert date columns to datetime
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'])
pm_data['Tanggal'] = pd.to_datetime(pm_data['Tanggal'])

# Rename columns for consistency
pm_data.rename(columns={'Tanggal': 'Date'}, inplace=True)

# Filter data for the year 2020
aeronet_2020 = aeronet_data[aeronet_data['Date'].dt.year == 2020]
pm_2020 = pm_data[pm_data['Date'].dt.year == 2020]

# Merge datasets on 'Date'
merged_data = pd.merge(aeronet_2020, pm_2020, on='Date')

# Remove rows with NaN values in 'AOD_500nm' or 'PM10'
merged_data.dropna(subset=['AOD_500nm', 'PM10'], inplace=True)

# Selecting AOD 500 nm and PM10 for regression
X = merged_data['PM10']  # PM10 as the independent variable
y = merged_data['AOD_500nm']  # AOD 500nm as the dependent variable

# Add a constant to the independent variable for the intercept
X = sm.add_constant(X)

# Perform robust regression
model = sm.RLM(y, X, M=sm.robust.norms.HuberT())
results = model.fit()

# Print the summary of the regression results
print(results.summary())

# Plotting the results
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['PM10'], merged_data['AOD_500nm'], color='blue', label='Actual Data')
predicted_values = results.predict(X)
plt.plot(merged_data['PM10'], predicted_values, color='red', label='Robust Regression Line')
plt.xlabel('PM10 (μg/m³)')
plt.ylabel('AOD 500nm')
plt.legend()
plt.show()

# Install necessary libraries
!pip install pandas --upgrade
!pip install matplotlib --upgrade

# Import libraries
import pandas as pd
import numpy as np

# Load data from the uploaded files
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'
kebonjeruk_data_path = '/content/drive/MyDrive/DATA SKRIPSI PALING FIXXXXAX/KebonJeruk2020-2022.xlsx'

# Read the Excel files using pandas, ensuring placeholders are replaced immediately
aeronet_data = pd.read_excel(aeronet_data_path)
kebonjeruk_data = pd.read_excel(kebonjeruk_data_path)

# Replace placeholders with NaN immediately after loading
aeronet_data.replace('---', np.nan, inplace=True)
kebonjeruk_data.replace('---', np.nan, inplace=True)

# Convert columns to the appropriate type after replacing placeholders
kebonjeruk_data['PM10'] = pd.to_numeric(kebonjeruk_data['PM10'], errors='coerce')

# Convert date columns to datetime ensuring correct date parsing
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'], errors='coerce')
kebonjeruk_data['Tanggal'] = pd.to_datetime(kebonjeruk_data['Tanggal'], errors='coerce')

# Merge datasets on date
data = pd.merge(aeronet_data, kebonjeruk_data, left_on='Date', right_on='Tanggal', how='inner')

# Ensure all relevant columns are numeric, now that placeholders are handled
data['PM10'] = pd.to_numeric(data['PM10'], errors='coerce')
data['Suhu Udara'] = pd.to_numeric(data['Suhu Udara'], errors='coerce')
data['PM10'] = pd.to_numeric(data['PM10'], errors='coerce')

# Specify the months for analysis (March to October)
months = [3, 4, 5, 6, 7, 8, 9, 10]  # March to October
data['Month'] = data['Date'].dt.month
filtered_data = data[data['Month'].isin(months)]

# Separate the data by year
data_2020 = filtered_data[filtered_data['Date'].dt.year == 2020]
data_2021 = filtered_data[filtered_data['Date'].dt.year == 2021]

# Calculate correlation matrices
correlation_2020 = data_2020[['AOD_500nm', 'PM10', 'PM10', 'Suhu Udara', 'PM10']].corr()
correlation_2021 = data_2021[['AOD_500nm', 'PM10', 'PM10', 'Suhu Udara', 'PM10']].corr()

# Display the correlation matrices
print("Correlation Matrix for 2020:")
print(correlation_2020)
print("\nCorrelation Matrix for 2021:")
print(correlation_2021)



import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Load the data from the provided Excel file
file_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'
data = pd.read_excel(file_path)

# Extract month from the Date column
data['Month'] = data['Date'].dt.month

# Define the specific months for each zenith angle category
specific_months = {
    '< 45°': [3],        # July
    '45°-75°': [7],      # March
    '> 75°': [1]         # January
}

# Create a new mapping of month to zenith category based on the specific months defined
def map_month_to_zenith_category(month):
    if month in specific_months['< 45°']:
        return '< 45°'
    elif month in specific_months['45°-75°']:
        return '45°-75°'
    elif month in specific_months['> 75°']:
        return '> 75°'
    else:
        return None

# Apply the function to create a new column for the specific zenith categories
data['Specific_Zenith_Category'] = data['Month'].apply(map_month_to_zenith_category)

# Filter the data to only include rows with a specific zenith category
specific_zenith_data = data[data['Specific_Zenith_Category'].notnull()]

# Calculate mean AOD_500nm for each specific zenith angle category
mean_aod_by_specific_zenith = specific_zenith_data.groupby('Specific_Zenith_Category')['AOD_500nm'].mean().reset_index()

# Replace the values in Specific_Zenith_Category column
mean_aod_by_specific_zenith['Specific_Zenith_Category'] = mean_aod_by_specific_zenith['Specific_Zenith_Category'].replace({
    '45°-75°': '< 45°',
    '< 45°': '45°-75°',
    '> 75°': '> 75°'
})

# Create a line chart for mean AOD_500nm across specific zenith angle categories
plt.figure(figsize=(8, 5))
plt.plot(mean_aod_by_specific_zenith['Specific_Zenith_Category'], mean_aod_by_specific_zenith['AOD_500nm'], marker='o', color='teal', linestyle='-')
plt.xlabel('Kategori Sudut Zenith Matahari')
plt.ylabel('AOD_500nm')
plt.ylim(0, max(mean_aod_by_specific_zenith['AOD_500nm']) + 0.1)  # Add some space above the highest point
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error

# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'  # Replace with your actual file path
environmental_data_path = '/content/drive/MyDrive/Skripci/BundaranHI2020-2022.xlsx'  # Replace with your actual file path

# Load the datasets
aeronet_data = pd.read_excel(aeronet_data_path)
environmental_data = pd.read_excel(environmental_data_path)

# Ensure 'Tanggal' and 'Date' are in datetime format
environmental_data['Tanggal'] = pd.to_datetime(environmental_data['Tanggal'])
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'])

# Filter the datasets for the year 2020
aeronet_2020 = aeronet_data[aeronet_data['Date'].dt.year == 2020]
environmental_2020 = environmental_data[environmental_data['Tanggal'].dt.year == 2020]

# Specify the months explicitly (March to October)
months = [3, 4, 5, 6, 7, 8, 9, 10]
aeronet_2020 = aeronet_2020[aeronet_2020['Date'].dt.month.isin(months)]
environmental_2020 = environmental_2020[environmental_2020['Tanggal'].dt.month.isin(months)]

# Convert 'PM10' to numeric and handle non-numeric entries
environmental_2020['PM10'] = pd.to_numeric(environmental_2020['PM10'], errors='coerce')

# Merge datasets on 'Date'
merged_data_2020 = pd.merge(aeronet_2020, environmental_2020, left_on='Date', right_on='Tanggal', how='inner')

# Drop rows with any NaN values in 'AOD_500nm' or 'PM10'
merged_data_2020.dropna(subset=['AOD_500nm', 'PM10'], inplace=True)

# Perform linear regression with AOD as independent variable and PM25 as dependent variable
regression_results_PM25 = linregress(merged_data_2020['AOD_500nm'], merged_data_2020['PM10'])

# Calculate predicted PM25 values
predicted_PM25 = regression_results_PM25.intercept + regression_results_PM25.slope * merged_data_2020['AOD_500nm']

# Calculate RMSE for PM25 predictions
rmse_PM25 = np.sqrt(mean_squared_error(merged_data_2020['PM10'], predicted_PM25))

# Prepare regression line data for plotting
x_values = np.linspace(merged_data_2020['AOD_500nm'].min(), merged_data_2020['AOD_500nm'].max(), 100)
y_values = regression_results_PM25.intercept + regression_results_PM25.slope * x_values

# Creating the scatter plot and regression line
plt.figure(figsize=(10, 6))
plt.scatter(merged_data_2020['AOD_500nm'], merged_data_2020['PM10'], color='blue', label='Data Aktual')
plt.plot(x_values, y_values, color='red', label='Regresi Linear')

# Annotating the plot with the regression equation, R^2, P-value, and RMSE
annotation_text = (f'y = {regression_results_PM25.slope:.4f}x + {regression_results_PM25.intercept:.4f}\n'
                   f'$R^2$ = {regression_results_PM25.rvalue**2:.4f}\n'
                   f'$p$-value = {regression_results_PM25.pvalue:.4e}\n'
                   f'RMSE = {rmse_PM25:.4f}')
plt.annotate(annotation_text, xy=(1.02, 0.5), xycoords='axes fraction', fontsize=12, ha='left', va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))

# Setting the labels and title
plt.xlabel('AOD 500nm')
plt.ylabel('PM10 (μg/m³)')
plt.legend()

# Adjust layout to make room for the annotation
plt.tight_layout(rect=[0, 0, 0.8, 1])  # Adjust the right margin to 0.8 to make space for the annotation

plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error

# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'  # Replace with your actual file path
environmental_data_path = '/content/drive/MyDrive/Skripci/BundaranHI2020-2022.xlsx'  # Replace with your actual file path

# Load the datasets
aeronet_data = pd.read_excel(aeronet_data_path)
environmental_data = pd.read_excel(environmental_data_path)

# Ensure 'Tanggal' and 'Date' are in datetime format
environmental_data['Tanggal'] = pd.to_datetime(environmental_data['Tanggal'])
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'])

# Filter the datasets for the year 2020
aeronet_2020 = aeronet_data[aeronet_data['Date'].dt.year == 2021]
environmental_2020 = environmental_data[environmental_data['Tanggal'].dt.year == 2021]

# Specify the months explicitly (March to October)
months = [3, 4, 5, 6, 7, 8, 9, 10]
aeronet_2020 = aeronet_2020[aeronet_2020['Date'].dt.month.isin(months)]
environmental_2020 = environmental_2020[environmental_2020['Tanggal'].dt.month.isin(months)]

# Convert 'PM2.5' to numeric and handle non-numeric entries
environmental_2020['PM10'] = pd.to_numeric(environmental_2020['PM10'], errors='coerce')

# Merge datasets on 'Date'
merged_data_2020 = pd.merge(aeronet_2020, environmental_2020, left_on='Date', right_on='Tanggal', how='inner')

# Drop rows with any NaN values in 'AOD_500nm' or 'PM2.5'
merged_data_2020.dropna(subset=['AOD_500nm', 'PM10'], inplace=True)

# Perform linear regression with AOD as independent variable and PM25 as dependent variable
regression_results_PM25 = linregress(merged_data_2020['AOD_500nm'], merged_data_2020['PM10'])

# Calculate predicted PM25 values
predicted_PM25 = regression_results_PM25.intercept + regression_results_PM25.slope * merged_data_2020['AOD_500nm']

# Calculate RMSE for PM25 predictions
rmse_PM25 = np.sqrt(mean_squared_error(merged_data_2020['PM10'], predicted_PM25))

# Prepare regression line data for plotting
x_values = np.linspace(merged_data_2020['AOD_500nm'].min(), merged_data_2020['AOD_500nm'].max(), 100)
y_values = regression_results_PM25.intercept + regression_results_PM25.slope * x_values

# Creating the scatter plot and regression line
plt.figure(figsize=(10, 6))
plt.scatter(merged_data_2020['AOD_500nm'], merged_data_2020['PM10'], color='blue', label='Data Aktual')
plt.plot(x_values, y_values, color='red', label='Regresi Linear')

# Annotating the plot with the regression equation, R^2, P-value, and RMSE
annotation_text = (f'y = {regression_results_PM25.slope:.4f}x + {regression_results_PM25.intercept:.4f}\n'
                   f'$R^2$ = {regression_results_PM25.rvalue**2:.4f}\n'
                   f'$p$-value = {regression_results_PM25.pvalue:.4e}\n'
                   f'RMSE = {rmse_PM25:.4f}')
plt.annotate(annotation_text, xy=(1.02, 0.5), xycoords='axes fraction', fontsize=12, ha='left', va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))

# Setting the labels and title
plt.xlabel('AOD 500nm')
plt.ylabel('PM10 (μg/m³)')
plt.legend()

# Adjust layout to make room for the annotation
plt.tight_layout(rect=[0, 0, 0.8, 1])  # Adjust the right margin to 0.8 to make space for the annotation

plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from sklearn.metrics import mean_squared_error

# Paths to the uploaded Excel files
# Load the datasets
aeronet_data_path = '/content/drive/MyDrive/Skripci/aeronet_combined_2020_2021_2022.xlsx'  # Replace with your actual file path
environmental_data_path = '/content/drive/MyDrive/Skripci/BundaranHI2020-2022.xlsx'  # Replace with your actual file path


# Load the datasets
aeronet_data = pd.read_excel(aeronet_data_path)
environmental_data = pd.read_excel(environmental_data_path)

# Ensure 'Date' and 'Tanggal' are in datetime format
aeronet_data['Date'] = pd.to_datetime(aeronet_data['Date'])
environmental_data['Tanggal'] = pd.to_datetime(environmental_data['Tanggal'])

# Filter the datasets for the years 2020 and 2021
aeronet_2020_2021 = aeronet_data[aeronet_data['Date'].dt.year.isin([2020, 2021])]
environmental_2020_2021 = environmental_data[environmental_data['Tanggal'].dt.year.isin([2020, 2021])]

# Convert 'PM25' to numeric and handle non-numeric entries.
environmental_2020_2021['PM2.5'] = pd.to_numeric(environmental_2020_2021['PM10'], errors='coerce')

# Merge datasets on 'Date'
merged_data_2020_2021 = pd.merge(aeronet_2020_2021, environmental_2020_2021, left_on='Date', right_on='Tanggal', how='inner')

# Drop rows with any NaN values in 'AOD_500nm' or 'PM25'
merged_data_2020_2021.dropna(subset=['AOD_500nm', 'PM10'], inplace=True)

# Create a new column for year-month grouping
merged_data_2020_2021['YearMonth'] = merged_data_2020_2021['Date'].dt.to_period('M')

# Group by this new 'YearMonth' and calculate mean for AOD and PM2.5
monthly_data = merged_data_2020_2021.groupby('YearMonth').agg({'AOD_500nm':'mean', 'PM10':'mean'}).reset_index()

# Convert 'YearMonth' back to datetime for plotting purposes
monthly_data['YearMonth'] = monthly_data['YearMonth'].dt.to_timestamp()

# Perform linear regression on the monthly mean data
monthly_regression_results = linregress(monthly_data['AOD_500nm'], monthly_data['PM10'])

# Calculate predicted PM25 values based on the regression results
monthly_predicted_pm25 = monthly_regression_results.intercept + monthly_regression_results.slope * monthly_data['AOD_500nm']

# Calculate RMSE for the monthly data predictions
monthly_rmse = np.sqrt(mean_squared_error(monthly_data['PM10'], monthly_predicted_pm25))

# Prepare regression line data for plotting
monthly_x_values = np.linspace(monthly_data['AOD_500nm'].min(), monthly_data['AOD_500nm'].max(), 100)
monthly_y_values = monthly_regression_results.intercept + monthly_regression_results.slope * monthly_x_values

# Creating the scatter plot and regression line
plt.figure(figsize=(10, 6))
plt.scatter(monthly_data['AOD_500nm'], monthly_data['PM10'], color='blue', label='Data Rataan Bulanan')
plt.plot(monthly_x_values, monthly_y_values, color='red', label='Regresi Linear')

# Annotating the plot with the regression equation, R^2, P-value, and RMSE
monthly_annotation_text = (f'y = {monthly_regression_results.slope:.4f}x + {monthly_regression_results.intercept:.4f}\n'
                           f'$R^2$ = {monthly_regression_results.rvalue**2:.4f}\n'
                           f'$p$-value = {monthly_regression_results.pvalue:.4e}\n'
                           f'RMSE = {monthly_rmse:.4f}')
plt.annotate(monthly_annotation_text, xy=(1.02, 0.5), xycoords='axes fraction', fontsize=12, ha='left', va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.95))

# Setting the labels and title
plt.xlabel('AOD 500nm')
plt.ylabel('PM10 (μg/m³)')
plt.legend()

# Adjust layout to make room for the annotation
plt.tight_layout(rect=[0, 0, 0.8, 1])  # Adjust the right margin to 0.8 to make space for the annotation

plt.show()