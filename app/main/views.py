from flask import render_template
from flask import request, redirect, url_for, session
from requests.auth import HTTPBasicAuth
import requests
import json
import os

from . import main


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/match', methods=['GET', 'POST'])
def match():
	# Receives user data from the html form
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
			api_base_url = os.getenv('API_BASE_URL')
			api_pointer = os.getenv('API_POINTER')
			admin = os.getenv('ADMIN')
			admin_pw = os.getenv('ADMIN_PW')
			# Put image into a dict
			my_img = {'image': image}

			# Check if server is awake
			response_checkup = requests.get(api_base_url, auth=HTTPBasicAuth(admin, admin_pw))
			if response_checkup.status_code == 200:
				# prepare headers for http request
				#content_type = 'image/jpeg'
				#headers = {'content-type': content_type}
				response_plant = requests.post(api_base_url + api_pointer, files=my_img, auth=HTTPBasicAuth(admin, admin_pw)) 
				print('\n', response_plant.status_code, '\n')

				# decode response
				api_results = json.loads(response_plant.text)
				session["recognized_plant"] = api_results
				print('Recognition_result:', api_results, '\n')
				print(request.url)

				# TODO: Get matching plant from database
				#def get_plant()
					#recognized_plant.plant_class
					#session['plant_info'] = Plantspecs.query.all()
					# return plant_info
					#pass

				return redirect(url_for('main.recognition'))

			else:
				print('Server does not respond at the moment.') 
			

	return render_template('match.html')


@main.route('/recognition')
def recognition():
	if "recognized_plant" in session:
		recognized_plant = session["recognized_plant"]
		#plant_info = session['plant_info']
		print('Session data:', recognized_plant)

		return render_template('recognition.html', recognized_plant=recognized_plant)
	else:
		return redirect(url_for("main.match"))

