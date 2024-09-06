# Import django forms that gives a good protection by default
from django import forms

# from .models import AssessmentParameters, TranslationTable

from django.utils.translation import gettext_lazy as _

# Import of recaptcha module to secure the Contact me form
from django_recaptcha.fields import ReCaptchaField


class contactMe(forms.Form):
    Email = forms.EmailField(required=True, label=_("Email"), label_suffix="")
    Subject = forms.CharField(required=True, label=_("Subject"), label_suffix="")
    Message = forms.CharField(widget=forms.Textarea, required=True, label=_("Message"), label_suffix="")
    captcha = ReCaptchaField(label_suffix="")


# class VulnerabilityDashboardForm(forms.Form):
#
#     def __init__(self, language):
#         super().__init__()
#
#         self.fields['hazard_dropdown'] = forms.ModelChoiceField(queryset=TranslationTable.objects.filter(
#             python_id__in=AssessmentParameters.objects.values_list('hazard', flat=True),
#             language__iexact=language).values_list('label', flat=True),
#                                                        initial=0, blank=False,
#                                                        widget=forms.Select(attrs={'id': 'hazard-dropdown'}))
#
#         self.fields['exposure_dropdown'] = forms.ModelChoiceField(queryset=TranslationTable.objects.filter(
#             python_id__in=AssessmentParameters.objects.values_list('exposure', flat=True),
#             language__iexact=language).values_list('label', flat=True),
#                                                        initial=0, blank=False,
#                                                        widget=forms.Select(attrs={'id': 'exposure-dropdown'}))
#
#         self.fields['impact_dropdown'] = forms.ModelChoiceField(queryset=TranslationTable.objects.filter(
#             python_id__in=AssessmentParameters.objects.values_list('impacts', flat=True),
#             language__iexact=language).values_list('label', flat=True),
#                                                        initial=0, blank=False,
#                                                        widget=forms.Select(attrs={'id': 'impact-dropdown'}))

