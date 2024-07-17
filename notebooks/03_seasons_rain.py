import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the provided CSV file
path = r'C:\Users\Zako3\OneDrive - University of Twente\Documents\ITC Courses\1st Year\Quartile 4\Weather Impact Analysis\Assessments\Drought Monitoring\outcomes\rain_ltm_filtered.csv'
df = pd.read_csv(path)

# Convert the 'system:time_start' column to datetime
df['system:time_start'] = pd.to_datetime(df['system:time_start'])

# Extract the year and month
df['Year'] = df['system:time_start'].dt.year
df['Month'] = df['system:time_start'].dt.month

# Define seasons
seasons = {
    'Gu': [4, 5, 6],
    'Xagaa': [6, 7, 8, 9, 10],
    'Deyr': [10, 11, 12],
    'Jilaal': [1, 2, 3, 12]
}

# Function to get season name
def get_season(month):
    for season, months in seasons.items():
        if month in months:
            return season
    return None

# Add season column
df['Season'] = df['Month'].apply(get_season)

# Plotting the seasonal rainfall using a box plot
plt.figure(figsize=(14, 7))
sns.boxplot(data=df, x='Season', y='precipitation', palette='muted')
plt.title('Seasonal Rainfall in Somaliland')
plt.xlabel('Season')
plt.ylabel('Rainfall (mm)')
plt.grid(True)
plt.savefig('Seasonal_Rainfall_Somaliland.png', dpi=300)
plt.show()
