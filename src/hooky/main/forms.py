from django import forms
from django.forms.models import inlineformset_factory
from hooky.main.models import UserProfile, User, Notification

class UserProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'github_username', 'github_key', 'github_key', 'key',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        instance.id = self.cleaned_data['id']
        instance.save()
        return instance

NotificationFormSet = inlineformset_factory(User, Notification, extra=1)
