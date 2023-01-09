"""geoadaptation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Those module are standard to manage the URL paths
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

# Import those module to translate text and add language patterns to your URL
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.conf.urls.i18n import i18n_patterns

# Import your views from your app (mine is coresite)
from coresite import views, plotly_vulnerability

from coresite.views import VulnerabityDashboard

# Import admin module to manage the admin panel
from django.contrib import admin
admin.autodiscover()

# Dotenv purpose is to hide secret key and login info from a .env file hidden on the server. Make sure you don't push
# your .env file on git and github!
from dotenv import load_dotenv
import os

urlpatterns = [
    # Hide the admin path to avoid BOT trying to brute force the default admin path
    path(str(os.getenv('RANDOM_ADMIN_URL')), admin.site.urls),
    # Point the path to the favicon in your static files.
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/geoadaptation.ico')))

]

# The patterns can be tweak to put the langage in the URL (/en/ or /fr/) with the i18n_ppaterns and then translate with
# _(name). You can use TemplateView for class based views and views.function for function based views depending on
# your needs. There are a lot of subtilities between the two, but in a nutshell, class views are great for reuse of code
# and simple task (such as generating a lot of very simple pages like most of my site is) and function views are better
# if you have a complex code (such as my dashboard for monitoring Urban Heat Island). It's not impossible to use
# class based views for those cases, but it takes more time to implement. The perks it's the reusability of class based
# views. It wasn't worth the extra effort in my case, since reusability wasn't my main concern.
urlpatterns += i18n_patterns (
    path("", TemplateView.as_view(template_name="home.html"), name="redirect"),
    path(_('Home'), TemplateView.as_view(template_name="home.html"), name='Home'),
    path(_('CCAP'), TemplateView.as_view(template_name="ccap.html"), name='CCAP'),
    path(_('Magog_ccap'), TemplateView.as_view(template_name="magog_ccap.html"), name='Magog_ccap'),
    path(_('Research'), TemplateView.as_view(template_name="research.html"), name='Research'),
    path(_('Magog_uhi'), views.magog_uhi, name='Magog_uhi'),
    path(_('Vulnerability_essay'), TemplateView.as_view(template_name="vulnerability_essay.html"),
         name='vulnerability_essay'),
    path(_('Tutorials'), TemplateView.as_view(template_name="tutorials.html"), name='Tutorials'),
    path(_('LoRa_tutorial'), TemplateView.as_view(template_name="lora_tutorial.html"), name='LoRa_tutorial'),
    path(_('Django_tutorial'), TemplateView.as_view(template_name="django_tutorial.html"), name='Django_tutorial'),
    path(pgettext_lazy(u'url', u'About'), views.contact_view, name='About'),
    path(pgettext_lazy(u'url', u'Email_sent'), views.email_sent, name='Email_sent'),
    path(_('Proof_concept_COVID'), views.proof_concept_COVID, name='Proof_concept_COVID'),
    path(_('Vulnerability-dashboard'), VulnerabityDashboard.as_view(), name='Vulnerability-dashboard'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
)
