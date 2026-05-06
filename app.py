from flask import Flask,render_template,request
import matplotlib
matplotlib.use('Agg')

import rasterio
import numpy as np

import matplotlib.pyplot as plt
import os
from sentinelhub import SHConfig,SentinelHubRequest,DataCollection,MimeType,CRS,BBox

# STORE LAST RESULT VALUES

last_mean = None
last_vegetation = None
last_health = None
last_lat = None
last_lon = None

app=Flask(__name__)
config=SHConfig()
config.sh_client_id="f30fe9cf-5f15-4d15-b27c-c37e9dab09e8"
config.sh_client_secret="nSmslK6jfmx4j8t7B1qY9jplclxP7JGy"

UPLOAD_FOLDER="uploads"
RESULT_FOLDER="static"

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/map")
def map():
    return render_template("map.html")
@app.route("/ndvi")
def ndvi_from_map():

    lat=float(request.args.get("lat"))
    lon=float(request.args.get("lon"))

    bbox = BBox([lon-0.01, lat-0.01, lon+0.01, lat+0.01], crs=CRS.WGS84)

    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["B04", "B08"],
            output: { bands: 1,
             sampleType:"FLOAT32" }
        };
    }

    function evaluatePixel(sample) {
        let ndvi=(sample.B08-sample.B04)/(sample.B08+sample.B04);
        return [ndvi];
    }
    """

    request_ndvi = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=("2024-01-01", "2024-12-31"),
            )
        ],
        responses=[
            SentinelHubRequest.output_response("default", MimeType.TIFF)
        ],
        bbox=bbox,
        size=[512,512],
        config=config,
    )

    ndvi = request_ndvi.get_data()[0]
    ndvi_clean = ndvi[~np.isnan(ndvi)]

    mean_ndvi = float(np.mean(ndvi_clean))

    vegetation_pixels = np.sum(ndvi_clean > 0.3)
    total_pixels = ndvi_clean.size

    vegetation_percentage = (vegetation_pixels / total_pixels) * 100


    if mean_ndvi > 0.6:
        health = "Healthy vegetation"
    elif mean_ndvi > 0.4:
        health = "Good vegetation"
    elif mean_ndvi > 0.2:
        health = "Moderate vegetation"
    elif mean_ndvi > 0:
        health = "Poor vegetation"
    else:
        health = "No vegetation"

    plt.imshow(ndvi, cmap="RdYlGn",vmin=-1,vmax=1)
    plt.colorbar()

    result_path="static/result.png"
    plt.savefig(result_path)
    plt.close()

    # return f'''
    # <h2>NDVI Result</h2>

    # <img src="/static/result.png">

    # <h3>Mean NDVI: {round(mean_ndvi,3)}</h3>

    # <h3>Vegetation Coverage: {round(vegetation_percentage,2)}%</h3>

    # <h3>Health: {health}</h3>

    # <a href="/map">Go Back</a>
    # '''
    # SAVE VALUES FOR DASHBOARD

    global last_mean, last_vegetation, last_health, last_lat, last_lon

    last_mean = round(mean_ndvi,3)
    last_vegetation = round(vegetation_percentage,2)
    last_health = health
    last_lat = lat
    last_lon = lon

    return render_template(
    "result.html",
    mean=round(mean_ndvi,3),
    vegetation=round(vegetation_percentage,2),
    health=health
    )

@app.route("/dashboard")

@app.route("/dashboard")
def dashboard():

    global last_mean, last_vegetation, last_health, last_lat, last_lon

    return render_template(
        "dashboard.html",
        mean=last_mean,
        vegetation=last_vegetation,
        health=last_health,
        lat=last_lat,
        lon=last_lon
    )
@app.route("/learn")
def learn():
    return render_template("learn.html")

if __name__=="__main__":
    app.run(debug=True)