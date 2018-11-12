from django.contrib.auth.forms import UserCreationForm
import django.forms as forms
from django.utils.translation import ugettext


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=ugettext("First name"),
                                 widget=forms.TextInput)
    last_name = forms.CharField(label=ugettext("Last name"),
                                widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'size': 30})
        self.fields['last_name'].widget = forms.TextInput(attrs={'size': 30})
