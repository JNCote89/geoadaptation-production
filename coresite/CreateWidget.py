# Import a custom script to create b64 images
from .CreateB64Img import create_b64_plt

# Import matplotlib to create figures
import matplotlib

# Configure the backend to use the most efficient one to render png images
matplotlib.use('agg')
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

# Import to connect with the database
from .models import magog_uhi

# Import to query the database
from django.db.models import Max, Avg

# Import to translate text
from django.utils.translation import gettext_lazy as _

# Import to manipulate date and time
import datetime

# List of sensors and their positionning related to the park
dict_of_devices_group = {
    "device_id_100m": ["a840415f3182bbd8", "a840416c2182d5bc", "a84041714182bbd6", "a84041bbb182d5bf",
                       "a84041919182d287"],
    "device_id_200m": ["a840412ad182bbd4", "a840415e2182bbd7"],
    "device_id_300m": ["a8404148e182d5be", "a840412eb182d2a6"],
    "device_id_400m": ["a84041543182d286"]}


# This function produce a table with the average and the max temperature of each class of sensors that is updated with
# every query by the user (num_date and num_time arguments).
def stats_selected_time(num_date, num_time):

    # Dictionnary to store the needed stats
    result_tmp_avg = {"device_id_100m": "", "device_id_200m": "", "device_id_300m": "", "device_id_400m": ""}
    result_tmp_max = {"device_id_100m": "", "device_id_200m": "", "device_id_300m": "", "device_id_400m": ""}

    # Conditions to make sure the input is valid.
    try:
        # Iteration through all the device group to get the average value.
        for device in dict_of_devices_group:
            result_tmp_avg[device] = round(list(magog_uhi.objects.filter(device_id__in=dict_of_devices_group[device],
                                                                         date__exact=num_date,
                                                                         time__hour__gt=int(num_time) - 1,
                                                                         time__hour__lte=int(num_time)).aggregate(
                Avg('temperature')).values())[0], 2)

        # Iteration through all the device group to get the maximum value.
        for device in dict_of_devices_group:
            result_tmp_max[device] = round(list(magog_uhi.objects.filter(device_id__in=dict_of_devices_group[device],
                                                                         date__exact=num_date,
                                                                         time__hour__gt=int(num_time) - 1,
                                                                         time__hour__lte=int(num_time)).aggregate(
                Max('temperature')).values())[0], 2)

        # Return the result for each cell in the table.
        return {"t_avg_100m": f"{result_tmp_avg['device_id_100m']} °C",
                "t_avg_200m": f"{result_tmp_avg['device_id_200m']} °C",
                "t_avg_300m": f"{result_tmp_avg['device_id_300m']} °C",
                "t_avg_400m": f"{result_tmp_avg['device_id_400m']} °C",
                "t_max_100m": f"{result_tmp_max['device_id_100m']} °C",
                "t_max_200m": f"{result_tmp_max['device_id_200m']} °C",
                "t_max_300m": f"{result_tmp_max['device_id_300m']} °C",
                "t_max_400m": f"{result_tmp_max['device_id_400m']} °C"}

    # If the input is invalid, return No Data
    except:
        t_avg_100m = t_avg_200m = t_avg_300m = t_avg_400m = "N/D"
        t_max_100m = t_max_200m = t_max_300m = t_max_400m = "N/D"

        # Return No Data or the real result depending on the validity of the input
        return {"t_avg_100m": t_avg_100m, "t_avg_200m": t_avg_200m, "t_avg_300m": t_avg_300m, "t_avg_400m": t_avg_400m,
                "t_max_100m": t_max_100m, "t_max_200m": t_max_200m, "t_max_300m": t_max_300m, "t_max_400m": t_max_400m}


# This function produce hourly graphs of the selected day by the user.
def graph_day(num_date):

    # The model return a datatime the first time you call the function. Then, Ajax return a string, thus
    # you need to make up for both cases with this condition.
    if type(num_date) == str:
        day = datetime.datetime.strptime(num_date, "%Y-%m-%d").day
        month = datetime.datetime.strptime(num_date, "%Y-%m-%d").month
        year = datetime.datetime.strptime(num_date, "%Y-%m-%d").year
        date = datetime.datetime.strptime(num_date, "%Y-%m-%d").date()
    else:
        day = num_date.day
        month = num_date.month
        year = num_date.year
        date = num_date

    # Dictionnary and list to store the needed axis values
    x_hours = []
    result_Tmax_hour = {"device_id_100m": [], "device_id_200m": [], "device_id_300m": [], "device_id_400m": []}
    result_Tavg_hour = {"device_id_100m": [], "device_id_200m": [], "device_id_300m": [], "device_id_400m": []}
    y_variables = {"max": result_Tmax_hour, "avg": result_Tavg_hour}

    # Iteration through all the recorded hours for the day. The sensors are not 100 % reliable, so it's possible to
    # have missing datas.
    for hour in list(magog_uhi.objects.filter(date__year=year,
                                              date__month=month).values_list('time__hour',
                                                                             flat=True).distinct().order_by(
        'time__hour')):
        x_hours.append(hour)

        # Then, for each valid hour, iteration through each device group to get the max and average temperature.
        for device in dict_of_devices_group:
            result_Tmax_hour[device].append((list(magog_uhi.objects.filter(date__year=year,
                                                                           date__month=month,
                                                                           date__day=day,
                                                                           time__hour=hour,
                                                                           device_id__in=dict_of_devices_group[
                                                                               device]).aggregate(
                Max('temperature')).values())[0]))

            result_Tavg_hour[device].append((list(magog_uhi.objects.filter(date__year=year,
                                                                           date__month=month,
                                                                           date__day=day,
                                                                           time__hour=hour,
                                                                           device_id__in=dict_of_devices_group[
                                                                               device]).aggregate(
                Avg('temperature')).values())[0]))

    graph_day_dict = {"max": "", "avg": ""}

    # Creation of the graph with Matplotlib
    for key, variable in y_variables.items():
        fig = Figure()
        ax = fig.subplots()
        fig.set_figheight(3.5)
        fig.set_figwidth(8)

        # Set a condition to translate the title depending on the key
        # (because dictionnary keys can't be translated on the fly)
        if key == "max":
            ax.set_title(_("Hourly maximum temperature on {date}").
                         format(date=date), fontdict={'fontsize': 12, "fontweight": 'bold'})
        else:
            ax.set_title(_("Hourly average temperature on {date}").
                         format(date=date), fontdict={'fontsize': 12, "fontweight": 'bold'})

        ax.plot(x_hours, variable["device_id_100m"], "o-b", ms=6, label="0-100 m")
        ax.plot(x_hours, variable["device_id_200m"], "*-g", ms=6, label="100-200 m")
        ax.plot(x_hours, variable["device_id_300m"], "x-", color='orange', ms=6, label="200-300 m")
        ax.plot(x_hours, variable["device_id_400m"], "x-r", ms=6, label="300-400 m")
        ax.tick_params(which="both", length=4, width=1, top=False, right=False)
        ax.grid(which='both', linewidth=0.25)
        ax.set_xlabel(_("Time"), fontdict={'fontsize': 10})
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        ax.xaxis.set_major_locator(MultipleLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(2))
        ax.set_xlim(xmin=0, xmax=24)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylabel("°C", fontdict={'fontsize': 10})
        ax.legend(bbox_to_anchor=(0, -0.4, 2, 0.5), loc='lower left', ncol=4)

        # Create a B64 image of the plot with a custom script from CreateB64Img.py
        graph_day_dict[key] = create_b64_plt(fig, 92)

        # Clear figure to replot data
        ax.cla()

    # Return both graphics, one for the average and one for the maximum temperature, stored in a dictionnary.
    return graph_day_dict


# This function produce daily graphs of the selected month by the user.
def graph_month(num_date):

    # The model return a datatime the first time you call the function. Then, Ajax return a string, thus
    # you need to make up for both cases
    if type(num_date) == str:
        day = datetime.datetime.strptime(num_date, "%Y-%m-%d").day
        month = datetime.datetime.strptime(num_date, "%Y-%m-%d").month
        year = datetime.datetime.strptime(num_date, "%Y-%m-%d").year
        date = datetime.datetime.strptime(num_date, "%Y-%m-%d").date()
    else:
        day = num_date.day
        month = num_date.month
        year = num_date.year
        date = num_date

    # Dictionnary and list to store the needed axis values
    x_days = []
    result_Tmax_hour = {"device_id_100m": [], "device_id_200m": [], "device_id_300m": [], "device_id_400m": []}
    result_Tavg_hour = {"device_id_100m": [], "device_id_200m": [], "device_id_300m": [], "device_id_400m": []}
    y_variables = {"max": result_Tmax_hour, "avg": result_Tavg_hour}

    # Iteration through all the recorded days for the month. The sensors are not 100 % reliable, so it's possible to
    # have missing datas.
    for day in list(magog_uhi.objects.filter(date__year=year,
                                             date__month=month).values_list('date__day', flat=True).distinct().order_by(
        'date__day')):
        x_days.append(day)

        # Then, for each valid hour, iteration through each device group to get the max and average temperature.
        for device in dict_of_devices_group:
            result_Tmax_hour[device].append((list(magog_uhi.objects.filter(date__year=year,
                                                                           date__month=month,
                                                                           date__day=day,
                                                                           device_id__in=dict_of_devices_group[
                                                                               device]).aggregate(
                Max('temperature')).values())[0]))

            result_Tavg_hour[device].append((list(magog_uhi.objects.filter(date__year=year,
                                                                           date__month=month,
                                                                           date__day=day,
                                                                           device_id__in=dict_of_devices_group[
                                                                               device]).aggregate(
                Avg('temperature')).values())[0]))

    graph_month_dict = {"max": "", "avg": ""}

    for key, variable in y_variables.items():
        fig = Figure()
        ax = fig.subplots()
        fig.set_figheight(3.5)
        fig.set_figwidth(8)

        # Set a condition to translate the title depending on the key
        # (because dictionnary keys can't be translated on the fly)
        if key == "max":
            ax.set_title(_("Daily maximum temperature on {year}-{month}").
                         format(year=year, month=month), fontdict={'fontsize': 12, "fontweight": 'bold'})
        else:
            ax.set_title(_("Daily average temperature on {year}-{month}").
                         format(year=year, month=month), fontdict={'fontsize': 12, "fontweight": 'bold'})

        ax.plot(x_days, variable["device_id_100m"], "o-b", ms=6, label="0-100 m")
        ax.plot(x_days, variable["device_id_200m"], "*-g", ms=6, label="100-200 m")
        ax.plot(x_days, variable["device_id_300m"], "x-", color='orange', ms=6, label="200-300 m")
        ax.plot(x_days, variable["device_id_400m"], "x-r", ms=6, label="300-400 m")
        ax.tick_params(which="both", length=4, width=1, top=False, right=False)
        ax.grid(which='both', linewidth=0.25)
        ax.set_xlabel(_("Day"), fontdict={'fontsize': 10})
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        ax.xaxis.set_major_locator(MultipleLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(2))
        ax.set_xlim(xmin=1, xmax=31)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylabel("°C", fontdict={'fontsize': 10})
        ax.legend(bbox_to_anchor=(0, -0.4, 2, 0.5), loc='lower left', ncol=4)

        # Create a B64 image of the plot with a custom script
        graph_month_dict[key] = create_b64_plt(fig, 92)
        # Clear figure to replot data
        ax.cla()

    # Return both graphics, one for the average and one for the maximum temperature, stored in a dictionnary.
    return graph_month_dict
