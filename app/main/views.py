from flask import render_template
from flask import request, redirect, url_for, session
import requests
import json
import os

from . import main


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/match', methods=['GET', 'POST'])
def match():
	if request.method == "POST":
		session.permanent = True
		if request.files:
			image = request.files["image"]

			# Raise exception if no file is selected
			if image.filename == "":
				print("No filename")
				return redirect(request.url)

			print(image)

			# Make API call
			api_url = os.getenv('API_URL')
			my_img = {'image': image}

			# prepare headers for http request
			#content_type = 'image/jpeg'
			#headers = {'content-type': content_type}
			response = requests.post(api_url, files=my_img) 

			print('\n', response.status_code, '\n')

			# decode response
			api_results = json.loads(response.text)
			session["recognized_plant"] = api_results
			print('Recognition_result:', api_results, '\n')
			print(request.url)

			return redirect(url_for('main.recognition'))

	return render_template('match.html')


@main.route('/recognition')
def recognition():
	if "recognized_plant" in session:
		recognized_plant = session["recognized_plant"]
		print('Session data:', recognized_plant)
		return render_template('recognition.html', recognized_plant=recognized_plant)
	else:
		return redirect(url_for("main.match"))

