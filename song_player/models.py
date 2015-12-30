from django.db import models
from djangotoolbox import fields
from django_mongodb_engine.contrib import MongoDBManager

class SongsUrl(models.Model):
	objects = MongoDBManager()
	primary_id = models.IntegerField(primary_key = True)
	url = models.TextField()
	created_at = models.DateTimeField()
