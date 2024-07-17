// This script is designed to work within the Google Earth Engine (GEE) environment to process and 
// analyze NDVI data from the MODIS satellite sensor, focusing specifically on the region of Somaliland. 
// The script is designed for the analysis of the paper paper titled "Spatiotemporal Analysis of 
// Agricultural Droughts in Somaliland: Integrating MODIS-derived Vegetation Indices and 
// CHIRPS Precipitation Estimates." 
// Vegetation Condition Index (VCI)
// Drought Monitoring in Somaliland
// Duration: 2005 until 2023
// © Abdillahi Osman Omar, 2024

Map.addLayer(somaliland, {color:'red'}, 'somaliland')
Map.centerObject(somaliland, 6)

var startYear = 2005;
var endYear = 2023;
print(startYear, endYear)

// Scale NDVI and filter collection
var ndviScaled = modis.map(function(image) {
  return image.select('NDVI').multiply(0.0001) // NDVI needs scaling with scale factor
    .copyProperties(image, ['system:time_start']);
});

// Calculate annual mean NDVI
var yearlyImages = ee.List.sequence(startYear, endYear).map(function(year) {
  var yearlyFilter = ndviScaled.filter(ee.Filter.calendarRange(year, year, 'year'));
  var yearlyMean = yearlyFilter.mean().set('year', year);
  return yearlyMean;
});
print(yearlyImages)

// Convert list to image collection
var yearlyCol = ee.ImageCollection.fromImages(yearlyImages);
print(yearlyCol)

// Calculate overall min and max NDVI
var minNdvi = yearlyCol.min();
var maxNdvi = yearlyCol.max();

// Calculate VCI for each year
var yearlyVCI = yearlyCol.map(function(image) {
  var vci = image.expression(
    '100 * (ndvi - minNdvi) / (maxNdvi - minNdvi)', {
      'ndvi': image,
      'minNdvi': minNdvi,
      'maxNdvi': maxNdvi
    }).rename('vci').toFloat(); // Ensure output is floating point
  return vci.set('year', image.get('year'));
});

// Visualisation parameters
var vciPalette = ['#a50026','#d73027','#f46d43','#fdae61',
  '#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837'];
var vciVisParams = {min: 0, max: 100, palette: vciPalette};

// Clip to the study area and add layer to map

var clippedVCI = yearlyVCI.map(function(image) {
  return image.clip(somaliland);
});


// Create a list of years from startYear to endYear
var years = Array.apply(null, {length: endYear - startYear + 1}).map(function(value, index) {
  return startYear + index;
});

// Creating a label and dropdown UI for selecting the year
var label = ui.Label('Select Year:');
var dropdown = ui.Select({
  items: years.map(String), // Convert years to string for display
  value: String(startYear), // Set initial value as the start year
  style: {stretch: 'horizontal'}
});

// Function to update the map based on the selected year from dropdown
dropdown.onChange(function(value) {
  Map.clear(); // Clear existing layers
  var year = parseInt(value);
  var layer = clippedVCI.filter(ee.Filter.eq('year', year)).first().clip(somaliland);
  Map.addLayer(layer, vciVisParams, 'VCI ' + year);
  label.setValue('VCI for the year: ' + year);
});

// Add the label and dropdown to the map
var panel = ui.Panel({
  widgets: [label, dropdown],
  style: {
    position: 'top-left',
    padding: '8px 15px'
  }
});
Map.add(panel);

// Assuming 'clippedVCI' is your ImageCollection with yearly VCI data
var startYear = 2005;
var endYear = 2023;

// Iterate over each year, set up an export task
for (var year = startYear; year <= endYear; year++) {
  (function(year) { // Create a closure to capture the current year
    var image = clippedVCI.filter(ee.Filter.eq('year', year)).first(); // Filter out the image for the given year
    var fileName = 'VCI_' + year;

    // Set up export parameters
    Export.image.toDrive({
      image: image,
      description: fileName,
      folder: 'earthengine/vci',
      fileNamePrefix: fileName,
      scale: 250, // Adjust scale based on your data's resolution and needs
      region: somaliland.geometry(), 
      fileFormat: 'GeoTIFF',
      maxPixels: 1e9 // Adjust as necessary to fit your export needs and computation
    });
  })(year);
}


