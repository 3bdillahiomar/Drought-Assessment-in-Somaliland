import os
import rasterio as rio
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from rasterio.plot import plotting_extent

# Define the paths of the dataset
regions_path = r"C:\Users\Zako3\Downloads\drought_somaliland\regions\somaliland_regions.gpkg"
ndvi_path = r"C:\Users\Zako3\Downloads\drought_somaliland\ndvi_2005_2023\earthengine-ndvi"

# Read the regions GeoPackage file
regions = gpd.read_file(regions_path)

# Get a list of all NDVI files in the directory
ndvi_files = sorted([f for f in os.listdir(ndvi_path) if f.endswith('.tif')])

# Create a figure with subplots
fig, axes = plt.subplots(nrows=3, ncols=6, figsize=(20, 10))
axes = axes.flatten()

# Define NDVI color mapping
cmap = plt.cm.YlGn
norm = Normalize(vmin=0, vmax=1)

# Loop through each NDVI file and plot it
for idx, ndvi_file in enumerate(ndvi_files):
    if idx >= len(axes):
        break

    ax = axes[idx]
    file_path = os.path.join(ndvi_path, ndvi_file)
    
    # Read the NDVI file
    try:
        with rio.open(file_path) as src:
            ndvi_data = src.read(1)
            extent = plotting_extent(src)
        
        # Plot the NDVI data
        im = ax.imshow(ndvi_data, cmap=cmap, norm=norm, extent=extent)
        
        # Overlay the region boundaries
        regions.boundary.plot(ax=ax, linewidth=1, edgecolor='black')
        
        # Set the title
        year = ndvi_file.split('NDVI')[1].split('.')[0]
        ax.set_title(f'NDVI {year}')
        ax.axis('off')
    
    except Exception as e:
        print(f"Error reading {ndvi_file}: {e}")
        ax.set_title(f'Error {ndvi_file}')
        ax.axis('off')

# Add colorbar
cbar_ax = fig.add_axes([0.92, 0.3, 0.02, 0.4])  # Positioning the colorbar outside the plot
cbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cbar_ax)
cbar.set_label('NDVI')

# Adjust layout and save the figure
plt.tight_layout(rect=[0, 0, 0.9, 1])  # Adjust layout to make room for the colorbar
plt.savefig('NDVI_Somaliland_Regions_2005_2023.png', dpi=300)
plt.show()
