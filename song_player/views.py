from .models import SongsUrl
from django.http import Http404
from datetime import datetime

from song_player.serializers import SongsUrlSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import song_config.settings
import logging

logger = logging.getLogger(__name__)


class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def add_song(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		data['created_at'] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		#Check to decide whether entry needs to be done in Incoming database of Outgoing
		data['primary_id'] = SongsUrl.objects.count()+1
		serializer = SongsUrlSerializer(data=data)
		
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
	
		return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




