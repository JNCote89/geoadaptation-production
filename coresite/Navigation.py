# Import to connect with the database
from .models import magog_uhi


# Custom function to retrieve the last data from the database and display it when the user connect to the page.
# No argument needed.
def initial_navigation():
    # Use of the filters provided by Django ORM (Object-Relational Mapper) to interact with the database. Here, we
    # retrieved the first and last day in the database to set the bound of the available date in the frontend.
    first_day = list(magog_uhi.objects.values_list('date').order_by('date').first())[0]
    last_day = list(magog_uhi.objects.values_list('date').order_by('-date').first())[0]
    times_list = list(magog_uhi.objects.
                      filter(date__exact='{date}'.format(date=last_day)).
                      values_list('time__hour', flat=True).
                      distinct().order_by('-time__hour'))

    check_times_list = []
    # Iterate through the data and make sure that there are 10 valid entries before returning a valid time to populate
    # the times list in the frontend. Else, return 0 that will be interprated as midnight by the create_map_frame in
    # CreateMap.py. Then, a check will be done to see if the 10 sensors have data. If it's not the case, an empty map
    # is returned with a message to choose another day.
    for time in times_list:
        if magog_uhi.objects.filter(date__exact='{date}'.format(date=last_day),
                                    time__hour='{time}'.format(time=time)).distinct('device_id').count() == 10:
            check_times_list.append(time)
    if not check_times_list:
        check_times_list.append(0)

    # Return the first day in the database, the last_day and the associate time list to populate the frontend user input
    # box.
    return {"first_day": first_day, "last_day": last_day, "times_list": check_times_list}


# Custom function to retrieve the input data from the user and update the time input box accordingly to show only the
# valid entries in the database.
def updateTimeList(num_time, num_date):

    # Conditions to make sure the input is valid. There are validations in the frontend, but never trust any frontend
    # validation, since anyone can injected anything.
    try:
        times_list = list(magog_uhi.objects.
                          filter(date__exact='{date}'.format(date=num_date)).values_list('time__hour', flat=True).
                          distinct().order_by('-time__hour'))

        check_times_list = []

        # Iterate through the data and make sure that there are 10 valid entries before returning a valid time to
        # populate the time list in the frontend. Else, return 0 that will be interprated as midnight by the
        # create_map_frame in CreateMap.py. Then, a check will be done to see if the 10 sensors have data. If it's not
        # the case, an empty map is returned with a message to choose another day.
        for time in times_list:
            if magog_uhi.objects.filter(date__exact='{date}'.format(date=num_date),
                                        time__hour='{time}'.format(time=time)).distinct('device_id').count() == 10:
                check_times_list.append(time)
        if not check_times_list:
            check_times_list.append(0)

        # This condition check if the time exist in the time list when a user choose a new date. If it's the case, keep
        # the same time. Else, pick the first time in the time list.
        if int(num_time) in check_times_list:
            check_time = num_time
        else:
            try:
                check_time = check_times_list[0]
            except:
                check_time = 0

        # Return the time list and a valid time in the list (either the same as the previous date or the first one in
        # the list if the same time yield an invalid selection.
        return {"times_list": check_times_list, "time": check_time}

    # If there is not a valid entry, return the default value of midnight. Additionnal checks will be done in
    # create_map_frame in CreateMap.py to deal with this.
    except:
        check_time = 0
        check_times_list = [0]

        return {"times_list": check_times_list, "time": check_time}
