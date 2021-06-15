# Import django forms that gives a good protection by default
from django import forms


from django.utils.translation import ugettext_lazy as _

# Import of recaptcha module to secure the Contact me form
from captcha.fields import ReCaptchaField

class contactMe(forms.Form):
    Email = forms.EmailField(required=True, label=_("Email"), label_suffix="")
    Subject = forms.CharField(required=True, label=_("Subject"), label_suffix="")
    Message = forms.CharField(widget=forms.Textarea, required=True, label=_("Message"), label_suffix="")
    captcha = ReCaptchaField(label_suffix="")
