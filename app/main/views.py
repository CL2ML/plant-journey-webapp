from flask import render_template
from flask import request, redirect
import requests
import json

from . import main


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/match', methods=['GET', 'POST'])
def match():
	if request.method == "POST":
		if request.files:
			image = request.files["image"]

			# Raise exception if no file is selected
			if image.filename == "":
				print("No filename")
				return redirect(request.url)

			print(image)

			# Make API call
			addr = 'http://127.0.0.1:8080'
			test_url = addr + '/api/classify'
			my_img = {'image': image}

			# prepare headers for http request
			#content_type = 'image/jpeg'
			#headers = {'content-type': content_type}
			response = requests.post(test_url, files=my_img) 

			print(response.status_code)

			# decode response
			print(json.loads(response.text))

			return redirect(request.url)




	return render_template('match.html')


