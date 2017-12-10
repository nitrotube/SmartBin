from __future__ import unicode_literals
from django.conf import settings
import os
from django.db import models

# Create your models here.

class Image(models.Model):
    image = models.FileField(upload_to=os.path.join(settings.BASE_DIR,"classify/newdata/"))
