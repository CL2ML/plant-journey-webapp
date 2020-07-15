from flask import render_template
from flask import request, redirect, url_for, session, current_app
from requests.auth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import requests
import json
import os

from . import main
from .. import db # Imports via the init file
from ..models import Plantspecs


@main.route('/')
def index():
	return render_template('index.html')


# Route: Page 2 ---------------------------------------------#
def allowed_image(filename):
	if not "." in filename:
		return False
	ext = filename.rsplit(".", 1)[1]
	if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False


def allowed_image_filesize(filesize):
	if int(filesize) <= current_app.config["MAX_IMAGE_FILESIZE"]:
		return True
	else:
		return False

#TODO: define function to retrieve db data
def get_db_data(rec_plant_name):
	plant_info = Plantspecs.query.filter_by(botanical_name=rec_plant_name).first_or_404()
	return plant_info.to_json()


@main.route('/match', methods=['GET', 'POST'])
def match():
	# Receives user data from the html form
	if request.method == "POST":
		session.permanent = True
		if request.files:
			print(request.cookies)
			if "filesize" in request.cookies:

				if not allowed_image_filesize(request.cookies["filesize"]):
					print("Filesize exceeded maximum limit")
					return redirect(request.url)
					
				image = request.files["image"]

				# Raise exception if no file is selected
				if image.filename == "":
					print("No filename")
					return redirect(request.url)
				
				print(image.filename)
				if allowed_image(image.filename):
					filename = secure_filename(image.filename)
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
						recognized_plant_name = session["recognized_plant"]['plant_class']
						print('Recognized plant name: ', recognized_plant_name)
						session['plant_info'] = get_db_data(recognized_plant_name)
						print('Plant data from db: ', session['plant_info'])

						return redirect(url_for('main.results'))

				else:
					print("That file extension is not allowed")
					return redirect(request.url)
			else:
				print("That file size is not allowed")
				return redirect(request.url)
			

	return render_template('match.html')


# @main.route('/recognition')
# def recognition():
# 	if "recognized_plant" in session:
# 		recognized_plant = session["recognized_plant"]
# 		plant_info = session['plant_info']
# 		print('Session data:', recognized_plant)

# 		return render_template('recognition.html', recognized_plant=recognized_plant, plant_info=plant_info)
# 	else:
# 		return redirect(url_for("main.match"))


@main.route('/results')
def results():
	if "recognized_plant" in session:
		recognized_plant = session["recognized_plant"]
		plant_info = session['plant_info']
		print('Session data:', recognized_plant)

		return render_template('results.html', recognized_plant=recognized_plant, plant_info=plant_info)
	else:
		return redirect(url_for("main.match"))

