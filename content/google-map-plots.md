Title: Plotting on Google Maps with gmplot
Date: 2019-08-29 12:00
Category: Python
Tags: Python, Google Maps
Slug: google-map-plots
Authors: Abhishek Pednekar
Summary: Add markers, polygons, heatmaps and more to Google Maps with Python
Cover: /static/images/black-gradient-article.jpg

In this post, we'll look at plotting different plot types on Google maps using the [gmplot](https://github.com/vgm64/gmplot) library in Python (v3.7). This is great if you need to highlight a specific section like a building, a street, a locality or other areas of interest on a map. **gmplot** provides a variety of plots out of the box.

1. Polygons with fills
2. Drop pins
3. Scatter points
4. Heatmaps
5. Gridlines 

We'll be using a simple example of plotting a route between two points and highlighting some areas of interest around them.

The complete code is available in this [Github repository](https://github.com/AbhishekPednekar84/codedisciples-blog-posts/tree/master/Index_4-google-map-plots)

### Google API Key
Before we start coding, we need to procure an API key from the [Google Cloud Platform Console](https://cloud.google.com/console/google/maps-apis/overview). Refer to this [link](https://developers.google.com/maps/documentation/javascript/get-api-key) for steps to obtain a new key. Google recommends restricting the API key to avoid unauthorized usage. For this demo, we will be running our app on a local Python http server. Hence, we will need to add **localhost** as a referrer. To do this, select *HTTP referrers (web sites)* under *Application restrictions* and add **localhost**. This will ensure that when we use the API key to generate a map from our localhost, Google will <u>not</U> deny the request. Failing to do this, will result in a *referrer not allowed* error.

![Google-API_Key]({static}/images/index4/google-api-key.jpg)

### Python code
Before we start writing out Python code, we will need to install the **gmplot** library. But before that, let's create a [virtual environment](https://www.youtube.com/watch?v=APOPm01BVrk). Once the environment is created and activated run `pip install gmplot`.

Once we import the library, we will create an object of the *GoogleMapPlotter* class. We can do this in one of two ways.

1. Passing the coordinates (latitude and longitude) of the desired location. We will also need to specify the level of the desired zoom
2. Using the *from_geocode* method and passing the name of our location

We'll be using the coordinates in our example. We will also need to specify our api key in the code. I'll be including this in an [environment vraiable](https://www.youtube.com/watch?v=IolxqkL7cD8). To generate coordinates, use this [website](https://www.latlong.net)

```
import os
from gmplot import gmplot

# Using the location coordinates
gmap = gmplot.GoogleMapPlotter(13.004707, 77.564177, 18)

# Using the location name
gmap = gmplot.GoogleMapPlotter.from_geocode("Bangalore")

gmap.apikey=os.environ.get(GOOGLE_API_KEY)
```

Now, let's start plotting. The coordinates above are of my old high school. We will add a marker for those coordinates and also specify additional coordinates to plot a polygon highlighting the school.

<u>**Marker**</u>:<br>
To add a **marker**, we will be passing the coordinates to the `marker` method. We will also include a color and a title for the marker. 

Please note that `gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"` needs to be included **only** for the Windows platform. This is due to an existing issue in the library.

```
gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
gmap.marker(13.004707, 77.564177, "#f0dd92", title="School")
```

<u>**Polygon**</u>:<br>
To add a **polygon with fill** to highlight our location, we will need to specify tuples of latitudes and longitudes and pass them to the `ploygon` method. We will also specify a color for the fill.

```
school_lats, school_longs = zip(
    *[
        (13.004885, 77.563913), (13.004728, 77.563907), (13.004563, 77.563908),
        (13.004558, 77.564166), (13.004563, 77.564455), (13.004730, 77.564450),
        (13.004882, 77.564450), (13.004882, 77.564176), 
    ]
)
gmap.polygon(school_lats, school_longs, "cornflowerblue")

gmap.draw("school_map.html")
```
The `draw` method will generate our map. In this case, I am generating the html file in the project folder. We can provide an absolute path to the method. As mentioned earlier, we will be using a local http server to view the map. To start the server run `python -m http.server` in the activated virtual environment. The local server runs on port 8000 by default. So our url will be *http://localhost:8000/school_map.html*.

I will also be dropping a point on, and adding a polygon around my old apartment. In the next section, we will plot couples our routes between the school and the apartment. The complete code will be available in the Github repository.

Here's what our map looks like at the moment.

![Marker-Polygon]({static}/images/index4/marker-polygon.jpg)

<u>**Line Plot**</u>:<br>
We will now plot two routes between the school and the apartment. To do this, we will first need the coordinates for multiples points along the routes and pass them to the `plot` method. The color and the thickness of the plot can also be specified in the method call.

```
# Coordinates - path one
path_one_lats, path_one_longs = zip(
    *[
        (13.004619, 77.563855), (13.003328, 77.563881), (13.002994, 77.563892),
        (13.002655, 77.563889), (13.002639, 77.563558), (13.002602, 77.562826),
    ]
)
gmap.plot(path_one_lats, path_one_longs, "cornflowerblue", edge_width=3.0)

# Coordinates - path two
path_two_lats, path_two_longs = zip(
    *[
        (13.003690, 77.563862), (13.003640, 77.562444),
        (13.002840, 77.562830), (13.002602, 77.562826),
    ]
)
gmap.plot(path_two_lats, path_two_longs, "green", edge_width=3.0)
```

Here's what our plots look like now. The alternate route is in green and has been specified only from the point where it diverges from the primary route.

![Routes]({static}/images/index4/routes.jpg)


<u>**Scatter Plots and Heatmaps**</u>:<br>
Next, we will add some **scatters** and **heatmaps** to indicate some areas of interest around the school. Agreed, that this is not the best use case for a scatter plot or a heatmap. But the idea here is to only show the implementation.

As was the case before, we will need to pass the desired coordinates to the `scatter` and the `heatmap` methods. In the `scatter` method, we will be passing `maker=False` since we do not want to drop pins on the coordinates. We will also be specifying the size and the color of the scatters.

```
# Coordinates - Scatters, Heatmaps
aoi_lats, aoi_longs = zip(
    *[
        (13.004716, 77.563684), (13.005855, 77.564780), (13.007455, 77.563552),
        (13.006760, 77.562985), (13.004268, 77.562464),
    ]
)
gmap.heatmap(aoi_lats, aoi_longs)
gmap.scatter(aoi_lats, aoi_longs, "#6e2142", marker=False, size=12)
```

**Scatter plot**:

![Scatters]({static}/images/index4/scatters.jpg)

**Heatmap**:

![Heatmaps]({static}/images/index4/heatmaps.jpg)