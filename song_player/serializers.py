from . import models

from rest_framework import serializers

class SongsUrlSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.SongsUrl
		fields = ('primary_id', 'url', 'created_at')