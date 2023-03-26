from django.db import models


# Create your models here.

class Message(models.Model):
    sentence = models.TextField()
    sentence_type = models.CharField(max_length=15)
   