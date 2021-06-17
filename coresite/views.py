# Usual librairies to manage rendering, post and get requests
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Librairies of custom scripts
from .Navigation import initial_navigation, updateTimeList
from .CreateMap import create_map_frame
from .CreateWidget import stats_selected_time, graph_day, graph_month
from .forms import contactMe

# Librairies to hide my e-mail inbox
from dotenv import load_dotenv
import os

# Librairies to manage the Contact me form
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

# Librairy for translation
from django.utils.translation import ugettext_lazy as _

# Librairy to limit the request per views to avoid spamming or too many requests that would burden the server over a
# normal use.
from ratelimit.decorators import ratelimit

# I had no choice to use the csp_exempt for the views for the dashboard of Magog urban heat island because it would
# have required a huge rewrite of my code to add nonce to the inline scripts and styles generated by Folium.
# You are more than welcome to suggested an improvment for security in this regard if you know a quick fix!
from csp.decorators import csp_exempt


# Use of a rate limit to avoid a flooding of requests to the server. A human user should not exceed 30 requests per
# minutes with a normal use.
@ratelimit(key='header:x-real-ip', method='POST', rate='30/m', block=True)
@csp_exempt
def magog_uhi(request):
    if request.method == "POST":

        # Retrieve the value from the date, time, colour and opacity input in the magog_uhi.html file. The opacity
        # is divide by 100 to get the % value.
        num_date = request.POST['num_date']
        num_time = request.POST['num_time']
        opacity = int(request.POST['opacity']) / 100
        color = request.POST['color']

        # Custom script from Navigation.py to update the time list according to the date the user choose. It also
        # return a valid time.
        nav_menu_updated = updateTimeList(num_time, num_date)

        # Custom script from CreateMap.py to update the map based on the user input.
        magog_map_updated = create_map_frame(num_date, nav_menu_updated["time"], opacity, color)

        # Custom script from CreateWidget.py to update the stats showed with the map.
        stats_updated = stats_selected_time(num_date, nav_menu_updated["time"])

        # Custom script from CreateWidget.py to update the graph showed with the map.
        daily_graph_updated = graph_day(num_date)
        monthly_graph_updated = graph_month(num_date)

        # This is a key thing to understand, you CAN'T return a render page following a post request. You must return
        # a Json and update every bit of the page via JQuery in the frontend based on the value you pass here.
        return JsonResponse({"times_list": nav_menu_updated["times_list"],
                             "time": nav_menu_updated["time"],
                             "magog_map_updated": magog_map_updated,
                             "t_avg_100m_updated": stats_updated["t_avg_100m"],
                             "t_avg_200m_updated": stats_updated["t_avg_200m"],
                             "t_avg_300m_updated": stats_updated["t_avg_300m"],
                             "t_avg_400m_updated": stats_updated["t_avg_400m"],
                             "t_max_100m_updated": stats_updated["t_max_100m"],
                             "t_max_200m_updated": stats_updated["t_max_200m"],
                             "t_max_300m_updated": stats_updated["t_max_300m"],
                             "t_max_400m_updated": stats_updated["t_max_400m"],
                             "daily_max_graph_updated": daily_graph_updated["max"],
                             "daily_avg_graph_updated": daily_graph_updated["avg"],
                             "monthly_max_graph_updated": monthly_graph_updated["max"],
                             "monthly_avg_graph_updated": monthly_graph_updated["avg"]})

    # If this is not a post request, render the page for the first time.
    else:
        # Default values for the input boxes
        nav_menu = initial_navigation()
        opacity = 0.75
        color = "jet"

        # Custom script from CreateMap.py to update the map based on the default values.
        magog_map = create_map_frame(nav_menu["last_day"], nav_menu["times_list"][0], opacity, color)

        # Dictionnary of a subset of colormap arguments to populate the list for the user to choose from.
        color = {"jet": "jet", "rainbow": "rainbow", "seismic": "seismic", "RdYlGn_r": "RdYlGn_r", "RdBu_r": "RdBu_r",
                 "gist_heat": "gist_heat", "afmhot": "afmhot", "hot": "hot", "cool": "cool", "winter": "winter",
                 "autumn": "autumn", "summer": "summer", "spring": "spring"}

        # Custom script from CreateWidget.py to show the stats of the most recent data in the database.
        stats = stats_selected_time(nav_menu["last_day"], nav_menu["times_list"][0])
        daily_graph = graph_day(nav_menu["last_day"])
        monthly_graph = graph_month(nav_menu["last_day"])

        # The context return a list of value to render in the HTML file. No need of using javascript to render them
        # the first time, only need to call the variable in the appropriate HTML tag with the use of {{ variable_name }}
        # One exception is the IFrame for the Magog map, to avoid using the {{ variable_name|safe }} tag that is
        # vulnerable to inject unsafe HTML, this one is return with the {{ variable_name|json_script }} and generate
        # in the magog_uhi.js.
        data = {"magog_map": magog_map,
                "opacity": opacity,
                "color": color,
                "first_day": str(nav_menu["first_day"]),
                "last_day": str(nav_menu["last_day"]),
                "times_list": nav_menu["times_list"],
                "t_avg_100m": stats["t_avg_100m"],
                "t_avg_200m": stats["t_avg_200m"],
                "t_avg_300m": stats["t_avg_300m"],
                "t_avg_400m": stats["t_avg_400m"],
                "t_max_100m": stats["t_max_100m"],
                "t_max_200m": stats["t_max_200m"],
                "t_max_300m": stats["t_max_300m"],
                "t_max_400m": stats["t_max_400m"],
                "daily_max_graph": daily_graph["max"],
                "daily_avg_graph": daily_graph["avg"],
                "monthly_max_graph": monthly_graph["max"],
                "monthly_avg_graph": monthly_graph["avg"]}

        # Return the rendering for magog_uhi.html file.
        return render(request, 'magog_uhi.html', context={"data": data})


# Use of a a rate limit to avoid spamming in combinaison with the recaptcha. The rate has been set to 3 requests
# per hour. The method is specify to POST, because we don't want to limit the access to the page, only the POST
# request following the push of the submit button by the user.
@ratelimit(key='header:x-real-ip', method='POST', rate='3/h')
def contact_view(request):

    # We test the condition of the rate limit. If true, we return a page without the form to inform the user that we
    # don't accept more than 3 request per hour per user.
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        context = _('To avoid any spamming of my inbox, only 3 messages can be sent '
                    'per hour per user based on your IP address. Thank you for your comprehension.')
        return render(request, 'about.html', {'form': context})

    # Else, we can provide the contactMe form created in the forms.py file.
    else:
        if request.method == 'GET':
            form = contactMe()

        # If the send button is pressed, the e-mail is sent.
        else:
            form = contactMe(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['Subject']
                from_email = form.cleaned_data['Email']

                # Because I'm using a homemade backend solution to avoid paying or using a third party app, I need to
                # append the email user to the message to see it in my inbox. It's by no mean a good practice, but
                # certainly enough for my basic needs.
                message = form.cleaned_data['Message'] + "\nfrom : " + form.cleaned_data['Email']
                try:
                    send_mail(subject, message, from_email, [str(os.getenv('EMAIL'))], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('Email_sent')
        return render(request, 'about.html', {'form': form})


# Redirect to a different page to confirm that the email went through.
def email_sent(request):
    return render(request, 'email_sent.html')
