# Import to connect with the databases
from .models import magog_sensor, magog_uhi

# Import a custom script to interpolate data
from .Interpolate import interpolate

# Import a custom script to create b64 images
from .CreateB64Img import create_b64_plt

# Import to create a legend
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.figure import Figure
from matplotlib import cm

# Import to ease array manipulation
import numpy as np

# Import to create a map
import folium
import folium.plugins
from folium.features import DivIcon

# Import to translate text
from django.utils.translation import ugettext_lazy as _


# Custom function to create a legend in Folium, since there are no function in Folium to do so (as of version 0.12.1).
def create_legend(color, min_temp, max_temp):
    # To remain coherent with the interpolation, we check if the gap between the max and the min temperature is at least
    # 6 °C. If not, we add and subtract 3 to make a gap of minimum 6.
    legend_min_temp = 0
    legend_max_temp = 0

    if max_temp - min_temp > 6:
        legend_min_temp = min_temp
        legend_max_temp = max_temp

    else:
        legend_min_temp = min_temp - 3
        legend_max_temp = max_temp + 3

    # Creation of a BBox plot to create a continuous color scale.
    fig = Figure()
    ax = fig.subplots()
    bbox0 = Bbox.from_bounds(0, 0, 1, 1)
    bbox = TransformedBbox(bbox0, ax.transAxes)

    # Since we use the same argument of colormap in the legend and the interpolate layer, the result match. The color
    # parameter is set by the user from the color_selector in the magog_uhi.html file
    bbox_image = BboxImage(bbox, cmap=cm.get_cmap(color, 256))
    fig.set_figheight(1.5)
    fig.set_figwidth(6)
    fig.patch.set_alpha(0.7)

    # Create 256 spaces to be filled with each color of the colormap created previously
    a = np.arange(256).reshape(1, 256)
    bbox_image.set_data(a)
    ax.add_artist(bbox_image)
    ax.set_title(_("Interpolation scale for temperature"), fontweight="bold", fontsize=18)
    ax.set_xlabel("°C", fontdict={'fontsize': 16})
    ax.axes.margins(0)

    # The axis are set according to the minimum and maximum temperature of the data that come from the function
    # create_map_frame (the legend function is call within this function) in order to have matching colors with the
    # same bounds
    ax.set_xlim(legend_min_temp, legend_max_temp)
    ax.tick_params(labelsize=14)
    ax.set_frame_on(False)
    ax.axes.get_yaxis().set_visible(False)

    # Create a B64 image of the plot with a custom script from CreateB64Img.py
    legend_b64 = create_b64_plt(fig, 50)

    return legend_b64


# Custom function from CreateMap.py to create a map with Folium based on user inputs and the database data
def create_map_frame(num_date, num_time, opacity, color):
    # It's easier to control the rendering of the map in the HTML file if you put it in a figure.
    f = folium.Figure(width=700, height=500)
    m = folium.Map(location=[45.2670, -72.1445], zoom_start=15).add_to(f)

    # Working with custompane allow to control the order in which the layers are rendered via the z_index parameter.
    # Look at the doc to get the default parameters. Here the pane is inititialized and will be used later in the
    # ImageOverlay function.
    folium.map.CustomPane(name='custompane', z_index=500).add_to(m)

    # The feature goup allows to control the layers selection
    fg = folium.FeatureGroup(name='Espace St-Luc')
    m.add_child(fg)

    # This polygon show the boundary of the park. Since it was a fairly simple one, I created it directly here instead
    # of using a GeoJson (which would have been a better option for more complicated purposes).
    folium.vector_layers.Polygon(
        ((45.26880, -72.13676), (45.26794, -72.13722),
         (45.26809, -72.13789), (45.26685, -72.13846),
         (45.26675, -72.13796), (45.26840, -72.13501),
         (45.26880, -72.13676)), tooltip="Espace Saint-Luc", name="Espace Saint-Luc", weight=1,
        fill=True, fill_opacity=0, color="black").add_to(fg)

    # Empty list to store the appropriate data to interpolate
    lat_list = []
    lon_list = []
    temp_list = []

    # Condition to make sure the input is valid.
    if num_date is not None:
        # Condition to make sure we have data for all 10 sensors, otherwise the interpolation might look weird.
        if magog_uhi.objects.filter(date__exact='{date}'.format(date=num_date),
                                    time__hour='{time}'.format(time=num_time)).distinct('device_id').count() == 10:

            # Iteration through the 10 sensors in the sensors table to get their position and iteration through the
            # temperature table to get the actual temperature in the previous hour choose by the user.
            for device in magog_sensor.objects.values_list('device_id'):
                lat = \
                magog_sensor.objects.filter(device_id__iexact='{device_id}'.format(device_id=device[0])).values(
                    "web_lat")[
                    0]["web_lat"]
                lon = \
                magog_sensor.objects.filter(device_id__iexact='{device_id}'.format(device_id=device[0])).values(
                    "web_lon")[
                    0]["web_lon"]
                temp = magog_uhi.objects.filter(device_id__iexact='{device_id}'.format(device_id=device[0]),
                                                date__exact=num_date,
                                                time__hour__gt=int(num_time) - 1,
                                                time__hour__lte=int(num_time)).values("temperature")[0][
                    "temperature"]

                lat_list.append(float(lat))
                lon_list.append(float(lon))
                temp_list.append(float(temp))




            # Call the function to interpolate from a custom script from Interpolate.py. It returns a grid with the
            # temperature that can be displayed as an image.
            raster_interpolate = interpolate(lon_list, lat_list, temp_list)

            # Call the function previously wrote in this script to create a legend. This return an image that can be
            # displayed over the map.
            legend = create_legend(color, min(temp_list), max(temp_list))

            # Custom function to create the color on the interpolated grid. If there is no temperature value in a square,
            # it return a blank pixel (0,0,0,0). If there is a temperature, the color is set according to the colormap
            # choose by the user.
            def custom_color(x, color):
                if np.isnan(x):
                    return (0, 0, 0, 0)
                else:
                    color = cm.get_cmap(color, 256)
                    return color(x)

            # Use of ImageOverlay to display the interpolate raster. The grid is agnostic of any geospatial information,
            # we need to provide the boundaries, the projection and the origin. Once it's set, we can add the color by
            # calling the custom_color function, set the opacity according to the user and add this to the pane previously
            # created to put this layer on top of everything else.
            folium.raster_layers.ImageOverlay(raster_interpolate,
                                              [[min(lat_list), min(lon_list)],
                                               [max(lat_list), max(lon_list)]],
                                              mercator_project=True,
                                              origin="lower",
                                              colormap=lambda x: custom_color(x, color),
                                              pixelated=False,
                                              opacity=opacity,
                                              name="Interpolation",
                                              pane='custompane').add_to(m)

            # The created legend can be added via FloatImage. This is a general function that can be used to display
            # anything, not necessarily a legend, but it's pretty handy for this purpose.
            folium.plugins.FloatImage(legend, bottom=5, left=5).add_to(m)

            # Add the LayerControl button to allow user to turn on or off the park boundary and the interpolate raster
            # for temperature.
            folium.LayerControl().add_to(m)

            # Return a HTML frame to be displayed in magog_uhi.html
            f = m._repr_html_()
            return f

        # If we don't have proper data to interpolate, return an empty map with a message of No data
        # available for this day.
        else:
            folium.LayerControl().add_to(m)
            folium.map.Marker(
                [45.26685, -72.13846],
                icon=DivIcon(
                    icon_size=(250, 50),
                    icon_anchor=(255, -5),
                    html='<div style="font-size:14pt;background-color:rgba(255,255,255,0.95);">{message}</div>'.
                        format(message=_("No data for this day, please select another one")),
                )
            ).add_to(m)
            f = m._repr_html_()

            return f
