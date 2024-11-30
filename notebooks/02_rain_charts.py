# Rainfall charts of somaliland 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


path = r'...\rain_ltm.csv'
# Load the data from the rain ltm CSV file
rainfall_data = pd.read_csv(path)
rainfall_data.head()

# Convert the 'system:time_start' to datetime
rainfall_data['system:time_start'] = pd.to_datetime(rainfall_data['system:time_start'])

# Add year and month columns for grouping
rainfall_data['Year'] = rainfall_data['system:time_start'].dt.year
rainfall_data['Month'] = rainfall_data['system:time_start'].dt.month

# Aggregate data to annual and monthly levels
annual_rainfall = rainfall_data.groupby('Year')['precipitation'].sum()
monthly_avg_rainfall = rainfall_data.groupby('Month')['precipitation'].mean()
# Can you print the monthly average rainfall values per month?
print(monthly_avg_rainfall)


# Plotting Annual Total Rainfall
plt.figure(figsize=(12, 6))
sns.lineplot(x=annual_rainfall.index, y=annual_rainfall.values)
plt.title('Annual Total Rainfall Somaliland 1972-01-01 2024-06-01')
plt.ylabel('Total Rainfall (mm)')
plt.xlabel('Year')
plt.grid(True)
plt.show()

# Plotting Monthly Average Rainfall
plt.figure(figsize=(12, 6))
sns.barplot(x=monthly_avg_rainfall.index, y=monthly_avg_rainfall.values, palette="viridis")
plt.title('Monthly Average Rainfall')
plt.ylabel('Average Rainfall (mm)')
plt.xlabel('Month')
plt.xticks(ticks=range(12), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
plt.grid(True)
plt.show()

# Plotting Yearly Rainfall Variability
plt.figure(figsize=(16, 8))
sns.boxplot(x='Year', y='precipitation', data=rainfall_data)
plt.title('Yearly Rainfall Variability')
plt.ylabel('Rainfall (mm)')
plt.xlabel('Year')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Analyse rainfall performance in seasons 
# Define seasons
seasons = {
    'Gu': [4, 5, 6],
    'Xagaa': [6, 7, 8, 9, 10],
    'Deyr': [10, 11, 12],
    'Jilaal': [1, 2, 3, 12]
}

# Create a new column for season
rainfall_data['Season'] = 'None'
for season, months in seasons.items():
    rainfall_data.loc[rainfall_data['Month'].isin(months), 'Season'] = season

# Plotting Seasonal Rainfall
plt.figure(figsize=(12, 6))
sns.boxplot(x='Season', y='precipitation', data=rainfall_data)
plt.title('Seasonal Rainfall')
plt.ylabel('Rainfall (mm)')
plt.xlabel('Season')
plt.grid(True)
plt.show()

# Plot Monthly total rainfall in 2023
plt.figure(figsize=(12, 6))
sns.barplot(x='Month', y='precipitation', data=rainfall_data[rainfall_data['Year'] == 2023], palette="viridis")
plt.title('Monthly Total Rainfall in 2023')
plt.ylabel('Total Rainfall (mm)')
plt.xlabel('Month')
plt.xticks(ticks=range(12), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
plt.grid(True)
plt.show()

# How much was the total rainfall in 2023?
total_rainfall_2023 = rainfall_data[rainfall_data['Year'] == 2023]['precipitation'].sum()
print(f'Total Rainfall in 2023: {total_rainfall_2023:.2f} mm')

# Calculate total rainfall for whole years in the dataset year by year 
total_rainfall_by_year = rainfall_data.groupby('Year')['precipitation'].sum()
print(total_rainfall_by_year)

# make chart of total rainfall by year
plt.figure(figsize=(12, 6))
sns.lineplot(x=total_rainfall_by_year.index, y=total_rainfall_by_year.values)
plt.title('Total Rainfall by Year')
plt.ylabel('Total Rainfall (mm)')
plt.xlabel('Year')
plt.grid(True)
plt.show()

# calculate monthly average rainfall for each year
monthly_avg_rainfall_by_year = rainfall_data.groupby(['Year', 'Month'])['precipitation'].mean().reset_index()
monthly_avg_rainfall_by_year.rename(columns={'precipitation': 'Average_Rainfall'}, inplace=True)
print(monthly_avg_rainfall_by_year)


# Plotting Monthly Average Rainfall by Year
plt.figure(figsize=(16, 8))
sns.lineplot(x='Month', y='Average_Rainfall', hue='Year', data=monthly_avg_rainfall_by_year)
plt.title('Monthly Average Rainfall by Year')
plt.ylabel('Average Rainfall (mm)')
plt.xlabel('Month')
plt.xticks(ticks=range(12), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
plt.grid(True)
plt.show()

