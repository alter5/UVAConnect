#################
from django.forms import ModelForm
from django import forms
from users.models import Profile, Choice
from countable_field.widgets import CountableWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class createProfileForm(ModelForm):
    hobbies = forms.ModelMultipleChoiceField(queryset=Choice.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    bio = forms.CharField(required =False, widget=forms.Textarea(attrs={"rows":10, "cols":20}), label="Your Bio")
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'
    class Meta:
        model = Profile
        fields = ['major','food', 'movie', 'hobbies', 'bio', 'imageFile']
        labels = {
            'major':'Your Major',
            'food' : 'Favorite Food',
            'movie' : 'Favorite Movie',
            'hobbies' : 'Your Hobbies',
            'bio' : 'Your Bio', # This label doesn't appear for bio for some reason (maybe because a widget for bio is specified above)
            'imageFile' : "Upload New Profile Image"}
        


class updateProfileForm(ModelForm):
    hobbies = forms.ModelMultipleChoiceField(queryset=Choice.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    bio = forms.CharField(required =False, widget=forms.Textarea(attrs={"rows":10, "cols":20}), label="Your Bio")
    helper = FormHelper()
    helper.add_input(Submit('update', 'Update', css_class='btn-primary'))
    helper.form_method = 'POST'
    class Meta:
        model = Profile
        fields = ['major','food', 'movie', 'hobbies', 'bio', 'imageFile']
        labels = {
            'major':'Your Major',
            'food' : 'Favorite Food',
            'movie' : 'Favorite Movie',
            'hobbies' : 'Your Hobbies',
            'bio' : 'Your Bio',
            'imageFile' : "Upload New Profile Image"}
        
