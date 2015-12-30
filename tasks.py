from celery import Celery
import requests
import json

#Use celery to put tasks in redis queue 
app = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')

@app.task
def post(url, data):
	r = requests.post(url,  data=json.dumps(data))
	print r.content