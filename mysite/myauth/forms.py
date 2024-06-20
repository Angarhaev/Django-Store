from django import forms
from myauth.models import Profile


class ProfileForm(forms.ModelForm):
    pass


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
