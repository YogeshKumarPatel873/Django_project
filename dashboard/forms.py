from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','description']

class Dateinput(forms.DateInput):
    input_type='date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':Dateinput()}
        fields=['subject','title','description','due','is_finished']

class SearchForm(forms.Form):
    text=forms.CharField(max_length=100,label='Enter your search :')

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_complete']

class ConversionForm(forms.Form):
    CHOICES=[('length','Length'),('mass','Mass')]
    measurement=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
class LengthForm(forms.Form):
    CHOICES=[('yard','Yard'),('foot','Foot')]
    input=forms.CharField(required=False,label=False,widget=forms.TextInput(attrs={'type':'number','placeholder':'Enter the number :'}))    
    measur1=forms.CharField(label="",widget=forms.Select(choices=CHOICES))
    measur2=forms.CharField(label="",widget=forms.Select(choices=CHOICES))
class MassForm(forms.Form):
    CHOICES=[('pound','Pound'),('kilogram','Kilogram')]
    input=forms.CharField(required=False,label=False,widget=forms.TextInput(attrs={'type':'number','placeholder':'Enter the number :'}))    
    measur1=forms.CharField(label="",widget=forms.Select(choices=CHOICES))
    measur2=forms.CharField(label="",widget=forms.Select(choices=CHOICES))
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']








        