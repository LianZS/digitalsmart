from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OAuthyb(models.Model):
    """yb and User Bind"""
    yb_name = models.CharField(max_length=64)
    yb_id = models.CharField(max_length=64)  # yb_id
