# Import to connect with the database
from .models import magog_uhi


# Custom function to retrieve the last data from the database and display it when the user connect to the page.
# No argument needed.
def initial_navigation():
    # Use of the filters provided by Django ORM (Object-Relational Mapper) to interact with the database.
    first_day = list(magog_uhi.objects.values_list('date').order_by('date').first())[0]
    last_day = list(magog_uhi.objects.values_list('date').order_by('-date').first())[0]
    times_list = list(magog_uhi.objects.
                      filter(date__exact='{date}'.format(date=last_day)).
                      values_list('time__hour', flat=True).
                      distinct().order_by('-time__hour'))

    check_times_list = []

    # Iterate through the data and make sure that there are 10 valid entries before returning a valid time to populate
    # the times list in the frontend.
    for time in times_list:
        if magog_uhi.objects.filter(date__exact='{date}'.format(date=last_day),
                                    time__hour='{time}'.format(time=time)).distinct('device_id').count() == 10:
            check_times_list.append(time)

    # Return the first day in the database, the last_day and the associate time list to populate the frontend user input
    # box.
    return {"first_day": first_day, "last_day": last_day, "times_list": check_times_list}


# Custom function to retrieve the input data from the user and update the time input box accordingly to show only the
# valid entries in the database.
def updateTimeList(num_time, num_date):

    # Conditions to make sure the input is valid.
    try:
        times_list = list(magog_uhi.objects.
                          filter(date__exact='{date}'.format(date=num_date)).values_list('time__hour', flat=True).
                          distinct().order_by('-time__hour'))

        check_times_list = []

        # Iterate through the data and make sure that there are 10 valid entries before returning a valid time to
        # populate the time list in the frontend.
        for time in times_list:
            if magog_uhi.objects.filter(date__exact='{date}'.format(date=num_date),
                                        time__hour='{time}'.format(time=time)).distinct('device_id').count() == 10:
                check_times_list.append(time)

        # Those conditions check if the selected time exist in the new date selected by the user. If there are no valid
        # data, the last available time is choose for the user in the new list.
        if num_time == "":
            try:
                check_time = check_times_list[0]
            except:
                check_time = ""
        else:
            if int(num_time) in check_times_list:
                check_time = num_time
            else:
                try:
                    check_time = check_times_list[0]
                except:
                    check_time = ""

        # Return the time list and a valid time in the list (either the same as the previous date or the last one in the
        # list if the same time yield an invalid selection.
        return {"times_list": check_times_list, "time": check_time}

    except:
        pass
