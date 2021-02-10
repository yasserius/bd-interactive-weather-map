# Bangladesh Interactive Map of Weather Data
Choropleth (heatmap) of weather data from 2011 Census by Bangladesh Bureau of Statitics.

<img src="https://github.com/yasserius/bd-interactive-weather-map/blob/main/screenshot.PNG" height=500>

## Demo

https://bd-weather-map.herokuapp.com/

<br>

## Data

Source: [[bbs.gov.bd]](http://www.bbs.gov.bd/site/page/2888a55d-d686-4736-bad0-54b70462afda/District-Statistics)

The data was extracted from 64 different PDF files into a single table. You can find the CSV file of the cleaned and processed data [here](https://github.com/yasserius/bd-interactive-weather-map/blob/main/weather_data_cleaned.csv).

The data includes types such as:
- Maximum Temperature
- Minimum Temperature
- Humidity
- Rainfall

for the years 2008 to 2011.

### GeoJSON Shapefile of Bangladesh Districts

The shapefiles used for the choropleth can be found [here](https://github.com/yasserius/bangladesh_geojson_shapefile).

<br>

## Tools

This app was made using [Plotly Dash](https://plotly.com/dash/)

<br>

## Related Projects

- [Bangladesh District Statistics Dataset](https://github.com/yasserius/bd_district_statistics_dataset)
- [Bangladesh GeoJSON Shapefile](https://github.com/yasserius/bangladesh_geojson_shapefile)
