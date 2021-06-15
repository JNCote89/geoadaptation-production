# Import of numpy and scipy to interpolate data
import numpy as np
import scipy.interpolate


# Custom function to interpolate temperature data from the sensors. Take 3 parameters (the longitude, the latitude and
# the temperature of each sensor)
def interpolate(lon, lat, temp):

    # Colormap take arguments between 0 and 1, so we need to return normalised data.
    def normalise(x, min_temp, max_temp):

        # To avoid having very strong contrast between close data within 1 °C, a minimum scale of 6 °C is set. If the
        # threshold between the min/max is above 6, we can use the real data to normalize.
        if max_temp - min_temp > 6:
            return (x - min_temp) / (max_temp - min_temp)

        else:
            return (x - (min_temp - 3)) / ((max_temp + 3) - (min_temp - 3))

    # Transforming the python list in numpy array make the manipulation easier for the rest of the code.
    x_lon_station = np.array(lon)
    y_lat_station = np.array(lat)
    temperature_station = np.array(temp)

    # Create a pair of coordinate lon,lat
    points_stations = list(zip(x_lon_station, y_lat_station))

    # Set the resolution of the grid. Since 1° in lon,lat is equal to 111 km, that means a resolution of 0,00009° give
    # approximatively 10 meters of resolution. The greater the resolution, the longer the script takes to compute. 10 m
    # was the best performance/precision for this case.
    res = 0.00009

    # This create the extent of the grid based on the resolution choose and the min/max extent of the stations.
    x_range = np.arange(x_lon_station.min(), x_lon_station.max() + res, res)
    y_range = np.arange(y_lat_station.min(), y_lat_station.max() + res, res)

    # Creation of the actual grid
    grid_x, grid_y = np.meshgrid(x_range, y_range)

    # Interpolation of the temperature based on the created grid and the value of the sampling from the sensors.
    temp_interpolation = scipy.interpolate.griddata(points_stations, temperature_station, (grid_x, grid_y),
                                                    method="cubic")

    # The return grid is normalized first to be able to use colormap that takes values between 0 and 1.
    return normalise(temp_interpolation, temperature_station.min(), temperature_station.max())
