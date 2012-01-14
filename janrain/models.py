from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms



# Create your models here.
class RegisteredUser(User):

    provider_name=models.CharField(max_length=1024, blank=True)
    
