# NDVI Monitoring System

A web-based application for monitoring vegetation health using NDVI (Normalized Difference Vegetation Index) analysis with satellite imagery from Sentinel-2.

## About NDVI

The Normalized Difference Vegetation Index (NDVI) is a numerical indicator that uses the visible and near-infrared bands of the electromagnetic spectrum to assess whether the target being observed contains live green vegetation.

**NDVI Formula:**
```
NDVI = (NIR - RED) / (NIR + RED)
```

Where:
- NIR: Near-Infrared Band (B08)
- RED: Red Band (B04)

**NDVI Interpretation:**
- **> 0.6**: Healthy vegetation
- **0.4 - 0.6**: Good vegetation
- **0.2 - 0.4**: Moderate vegetation
- **0 - 0.2**: Poor vegetation
- **< 0**: No vegetation

## Features

- 🗺️ **Interactive Map Interface**: Select coordinates to analyze vegetation health
- 📊 **NDVI Analysis**: Real-time computation using Sentinel-2 satellite data
- 📈 **Vegetation Coverage**: Percentage calculation of vegetated pixels
- 💚 **Health Classification**: Automatic health status assessment
- 📸 **Visualization**: NDVI heatmap generation
- 📚 **Educational Resources**: Learn about vegetation monitoring

## Project Structure

```
NDVI_Monitoring_System/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static files (CSS, JS, images)
│   └── result.png       # Generated NDVI heatmap
├── templates/           # HTML templates
│   ├── home.html        # Home page
│   ├── map.html         # Interactive map interface
│   ├── result.html      # Results display
│   ├── dashboard.html   # Results dashboard
│   └── learn.html       # Educational content
└── uploads/             # User uploaded files
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Sentinel Hub API account (free tier available)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/HadiyaSalma27/NDVI_Monitoring_System.git
   cd NDVI_Monitoring_System
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Sentinel Hub credentials**
   
   Update the credentials in `app.py`:
   ```python
   config.sh_client_id = "your_client_id"
   config.sh_client_secret = "your_client_secret"
   ```
   
   Get your credentials from [Sentinel Hub](https://www.sentinel-hub.com/)

5. **Run the application**
   ```bash
   python app.py
   ```
   
   The application will be available at `http://localhost:5000`

## Usage

1. **Navigate to the application**: Open your browser and go to `http://localhost:5000`

2. **Select a location on the map**: Click on the interactive map to choose a location

3. **View NDVI results**: 
   - See the NDVI heatmap visualization
   - Check vegetation coverage percentage
   - View vegetation health classification

4. **Access the dashboard**: View your analysis results with location details

5. **Learn more**: Visit the educational section to understand NDVI and vegetation monitoring

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Data Processing**: NumPy, Rasterio
- **Visualization**: Matplotlib
- **Satellite Data**: Sentinel Hub API (Sentinel-2 L2A)
- **Frontend**: HTML/CSS/JavaScript
- **Geospatial**: Rasterio, Sentinelhub-py

## Key Dependencies

- `flask`: Web framework
- `sentinelhub`: Sentinel Hub API client
- `rasterio`: Raster data processing
- `numpy`: Numerical computing
- `matplotlib`: Data visualization
- `requests`: HTTP requests

## How It Works

1. **User selects a location**: Map interface provides coordinates (latitude, longitude)

2. **API Request**: Queries Sentinel-2 Level 2A satellite imagery for the region
   - Time range: Full year (2024-01-01 to 2024-12-31)
   - Area: ~2km x 2km around selected point
   - Resolution: 512x512 pixels

3. **NDVI Calculation**: 
   - Extracts B04 (red) and B08 (near-infrared) bands
   - Computes NDVI using the formula
   - Removes NaN values from calculations

4. **Analysis**:
   - Calculates mean NDVI value
   - Counts vegetation pixels (NDVI > 0.3)
   - Determines vegetation coverage percentage
   - Assesses health status

5. **Visualization**:
   - Generates NDVI heatmap with color scale (Red-Yellow-Green)
   - Stores result image
   - Displays results to user

## API Endpoints

- `GET /` - Home page
- `GET /map` - Interactive map interface
- `GET /ndvi?lat=<latitude>&lon=<longitude>` - Calculate NDVI for given coordinates
- `GET /dashboard` - View results dashboard
- `GET /learn` - Educational resources

## Notes

⚠️ **Important**: The API credentials in `app.py` are for demonstration purposes. Replace with your own credentials from Sentinel Hub.

## Getting Started with Sentinel Hub

1. Create a free account at [sentinel-hub.com](https://www.sentinel-hub.com/)
2. Create an OAuth client
3. Copy your Client ID and Client Secret
4. Update them in the application configuration

## Future Enhancements

- [ ] Time-series NDVI analysis
- [ ] Multi-location comparison
- [ ] Historical data trends
- [ ] Export analysis reports
- [ ] Machine learning predictions
- [ ] User authentication
- [ ] Database integration

## Troubleshooting

**Issue**: "API request failed" or "Unable to fetch satellite data"
- Verify your Sentinel Hub credentials are correct
- Check internet connection
- Ensure the location has available Sentinel-2 imagery

**Issue**: NDVI values are all NaN
- The location may lack sufficient cloud-free data
- Try a different time period
- Select a different geographic area

## License

This project is open source and available under the MIT License.

## Author

**HadiyaSalma27**
- GitHub: [@HadiyaSalma27](https://github.com/HadiyaSalma27)

## References

- [Sentinel Hub Documentation](https://www.sentinel-hub.com/docs/)
- [Sentinel-2 Data](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2)
- [NDVI Explanation](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index)
- [Rasterio Documentation](https://rasterio.readthedocs.io/)

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Last Updated**: May 2026
