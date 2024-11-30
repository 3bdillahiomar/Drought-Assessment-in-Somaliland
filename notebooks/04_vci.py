import os
import glob
import geopandas as gpd
from osgeo import gdal, ogr
import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Path to the directory containing all the TIFF files
directory = r"...vci\earthengine-vci"
districts_path = r"...somaliland_districts.gpkg"

# Get a list of all TIFF files in the directory
tiff_files = glob.glob(os.path.join(directory, "*.tif"))
tiff_files.sort()  # Ensure the files are sorted by year

# Read the districts GeoPackage file
districts = gpd.read_file(districts_path)

# Function to classify the VCI values
def classify_vci(data):
    conditions = np.zeros(data.shape, dtype=np.uint8)
    conditions[(data >= 60) & (data <= 100)] = 2  # Good
    conditions[(data >= 40) & (data < 60)] = 1    # Fair
    conditions[(data >= 0) & (data < 40)] = 0     # Poor
    return conditions

# Function to clip raster using GDAL
def clip_raster(input_raster, output_raster, shapefile):
    ds = gdal.Warp(output_raster,
                   input_raster,
                   format='GTiff',
                   cutlineDSName=shapefile,
                   cropToCutline=True,
                   dstNodata=-9999)
    ds = None  # Close the file

# Function to read and plot a single clipped TIFF file
def read_and_plot_tiff(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Read the first band
        classified_data = classify_vci(data)
        
        # Define a color map for the classified data
        cmap = ListedColormap(['red', 'yellow', 'green'])
        bounds = [0, 1, 2, 3]
        norm = plt.Normalize(vmin=0, vmax=2)
        
        plt.figure(figsize=(10, 10))
        plt.imshow(classified_data, cmap=cmap, norm=norm)
        cbar = plt.colorbar(ticks=[0, 1, 2], boundaries=bounds)
        cbar.set_ticklabels(['Poor', 'Fair', 'Good'])
        cbar.set_label('VCI Condition')
        plt.title(f"VCI - {os.path.basename(file_path)}")
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

# Clip and visualize each TIFF file
for i, tiff_file in enumerate(tiff_files):
    clipped_tiff = f"clipped_{i}.tif"
    clip_raster(tiff_file, clipped_tiff, districts_path)
    read_and_plot_tiff(clipped_tiff)

# How many files are there in the directory?
num_files = len(tiff_files)
print(f"Number of TIFF files in the directory: {num_files}")

# Vizualise the districts
districts.plot()
plt.title('Somaliland Districts')
plt.show()

# vizualise the clipped tiff files in single plot
fig, axs = plt.subplots(3, 3, figsize=(15, 15))
for i, tiff_file in enumerate(tiff_files[:9]):
    with rasterio.open(tiff_file) as src:
        data = src.read(1)
        axs[i // 3, i % 3].imshow(data, cmap='viridis')
        axs[i // 3, i % 3].set_title(os.path.basename(tiff_file))
        axs[i // 3, i % 3].axis('off')
plt.tight_layout()

# vizualize the rest of the tiff files
fig, axs = plt.subplots(3, 3, figsize=(15, 15))
for i, tiff_file in enumerate(tiff_files[9:]):
    with rasterio.open(tiff_file) as src:
        data = src.read(1)
        axs[i // 3, i % 3].imshow(data, cmap='viridis')
        axs[i // 3, i % 3].set_title(os.path.basename(tiff_file))
        axs[i // 3, i % 3].axis('off')

plt.tight_layout()
plt.show()

# Vizualise in pairs the clipped tiff files with the districts
# Vizualise each distrct separately
# Clip based on the column dist_name in the districts file

# Get the unique district names
district_names = districts['dist_name'].unique()

# Clip and visualize each district separately
for district_name in district_names:
    district = districts[districts['dist_name'] == district_name]
    district_file = f"{district_name}.gpkg"
    district.to_file(district_file, driver='GPKG')
    
    for i, tiff_file in enumerate(tiff_files):
        clipped_tiff = f"clipped_{i}_{district_name}.tif"
        clip_raster(tiff_file, clipped_tiff, district_file)
        read_and_plot_tiff(clipped_tiff)

# Make statistics for each district and each year and save them in a csv file
# Create an empty DataFrame to store the statistics
import pandas as pd
statistics = pd.DataFrame(columns=['District', 'Year', 'Poor', 'Fair', 'Good'])

# Loop over each district and each year
for district_name in district_names:
    district = districts[districts['dist_name'] == district_name]
    district_file = f"{district_name}.gpkg"
    district.to_file(district_file, driver='GPKG')
    
    for i, tiff_file in enumerate(tiff_files):
        clipped_tiff = f"clipped_{i}_{district_name}.tif"
        clip_raster(tiff_file, clipped_tiff, district_file)
        
        with rasterio.open(clipped_tiff) as src:
            data = src.read(1)
            classified_data = classify_vci(data)
            poor = np.sum(classified_data == 0)
            fair = np.sum(classified_data == 1)
            good = np.sum(classified_data == 2)
            
            year = os.path.basename(tiff_file).split('_')[1].split('.')[0]
            statistics = statistics.append({'District': district_name, 'Year': year, 'Poor': poor, 'Fair': fair, 'Good': good}, ignore_index=True)



# Save the statistics to a CSV file
statistics.to_csv('district_statistics.csv', index=False)

