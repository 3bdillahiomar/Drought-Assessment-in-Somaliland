import os
import glob
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rasterstats import zonal_stats

# Path to the directory containing all the TIFF files
directory = r"C:\Users\Zako3\Downloads\drought_somaliland\ndvi_2005_2023\earthengine-ndvi"
regions_path = r"C:\Users\Zako3\Downloads\drought_somaliland\regions\somaliland_regions.gpkg"

# Get a list of all TIFF files in the directory
tiff_files = glob.glob(os.path.join(directory, "*.tif"))
tiff_files.sort()  # Ensure the files are sorted by year

# Read the regions GeoPackage file
regions = gpd.read_file(regions_path)

# Initialize a DataFrame to store NDVI values
ndvi_df = pd.DataFrame()

# Loop through each NDVI file and calculate mean NDVI for each region
for tiff_file in tiff_files:
    # Extract the year from the filename (assuming the format "NDVIYYYY.tif")
    year = os.path.basename(tiff_file)[4:8]
    with rasterio.open(tiff_file) as src:
        ndvi_data = src.read(1)
        affine = src.transform
        # Calculate zonal statistics
        stats = zonal_stats(regions, ndvi_data, affine=affine, stats=['mean'])
        # Extract mean NDVI values for each region
        mean_ndvi = [stat['mean'] for stat in stats]
        # Add to DataFrame
        ndvi_df[year] = mean_ndvi

# Transpose DataFrame to have years as rows and regions as columns
ndvi_df = ndvi_df.T
ndvi_df.columns = regions['name_1']  # Assuming the region names are in a column named 'name_1'

# Calculate NDVI anomaly (deviation from mean)
ndvi_anomaly_df = ndvi_df - ndvi_df.mean()

# Classify NDVI anomaly into drought severity classes
def classify_drought(anomaly):
    if anomaly > 0:
        return 'No drought'
    elif 0 >= anomaly > -10:
        return 'Slight drought'
    elif -10 >= anomaly > -25:
        return 'Moderate drought'
    elif -25 >= anomaly > -50:
        return 'Severe drought'
    else:
        return 'Very severe drought'

# Apply classification to the anomaly dataframe
drought_classification_df = ndvi_anomaly_df.applymap(classify_drought)

# Combine the anomaly values with the classification
combined_df = pd.DataFrame(index=ndvi_anomaly_df.index)
for col in ndvi_anomaly_df.columns:
    combined_df[col + '_anomaly'] = ndvi_anomaly_df[col]
    combined_df[col + '_classification'] = drought_classification_df[col]

# Save the combined DataFrame to a CSV file
combined_df.to_csv('drought_classification.csv')

# Function to plot time series for each region
def plot_ndvi_time_series(ndvi_df):
    plt.figure(figsize=(15, 10))
    for region in ndvi_df.columns:
        plt.plot(ndvi_df.index, ndvi_df[region], label=region)

    plt.xlabel('Year')
    plt.ylabel('Mean NDVI')
    plt.title('Time Series of Mean NDVI for Each Region')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gca().set_xticklabels(ndvi_df.index.astype(int))
    plt.tight_layout()
    plt.show()

# Plot the time series for each region
plot_ndvi_time_series(ndvi_df)

# Display the drought classification for inspection
print(drought_classification_df)
