from django import forms
from .models import *
class mform(forms.ModelForm):
    class Meta():
        model=addproduct
        fields=['name','description','price','image','stock']

class myform(forms.ModelForm):
    class Meta():
        model=user
        fields=['address','phonenumber','image']