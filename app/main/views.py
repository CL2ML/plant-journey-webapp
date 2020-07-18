from flask import render_template
from flask import request, redirect, url_for, session, current_app
from requests.auth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import requests
import json
import os
import pandas as pd

from . import main
from .. import db # Imports via the init file
from ..models import Plantspecs, PlantSchema

# Init the marshmallow serialization schema
plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)


# Route: Page 1 - Landing Page  ---------------------------------------------#

@main.route('/')
def index():
	return render_template('index.html')


# Route: Page 2 - Matching options ---------------------------------------------#

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

# define function to retrieve db data
def get_db_recognized_plant(rec_plant_name):
	plant_info = Plantspecs.query.filter_by(botanical_name=rec_plant_name).first_or_404()
	result = plant_schema.dump(plant_info)
	return result


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
					print('Image:', image)

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
						#api_results = {'plant_class':'Aloe'}
						api_results = json.loads(response_plant.text)
						session["recognized_plant"] = api_results
						print('Recognition_result:', api_results, '\n')

						print(request.url)

						# Get matching plant from database
						recognized_plant_name = session["recognized_plant"]['plant_class']
						print('Recognized plant name: ', recognized_plant_name)
						session['plant_info'] = get_db_recognized_plant(recognized_plant_name)
						print('Plant data from db: ', session['plant_info'])


						return redirect(url_for('main.recognition'))

				else:
					print("That file extension is not allowed")
					return redirect(request.url)
			else:
				print("That file size is not allowed")
				return redirect(request.url)
			

	return render_template('match.html')


# Route: Page 3 - Recognition results ---------------------------------------------#

@main.route('/recognition')
def recognition():
	if "recognized_plant" in session:
		recognized_plant = session["recognized_plant"]
		print('Session data - recognized_plant:', recognized_plant)
		print('Session data - plant_info:', session['plant_info'])

		# Load the plant csv into a pandas data frame and filter out the recognized plant
		df = pd.read_csv('./app/static/images/links/plant_photos_db.csv', header=0)
		target_plant = df[df['botanical_name'] == recognized_plant['plant_class']]
		plant_url = target_plant.iloc[0]['final_source']
		print('plant_url:', plant_url)

		return render_template('recognition.html', recognized_plant=session["recognized_plant"], plant_info=session['plant_info'], plant_url=plant_url)
	else:
		return redirect(url_for("main.match"))


# Route: Page 4 - Matching filter ---------------------------------------------#

@main.route('/filter-plants', methods=['GET','POST'])
def filter_plants():
	# Receives user data from the html form
	if request.method == "POST":
		session.permanent = True
		# Save the request data to the session
		session['light'] = request.form.get('light')
		print('Session data - light:', request.form.get('light'))
		
		session['water'] = request.form.get('water')
		print('Session data - water:', request.form.get('water'))

		session['not_toxic'] = request.form.get('not_toxic')
		print('Session data - not_toxic:', session['not_toxic'])

		session['kids_toxic'] = request.form.get('kids_toxic')
		print('Session data - kids_toxic:', session['kids_toxic'])

		session['dogs_toxic'] = request.form.get('dogs_toxic')
		print('Session data - dogs_toxic:', session['dogs_toxic'])

		session['cats_toxic'] = request.form.get('cats_toxic')
		print('Session data - cats_toxic:', session['cats_toxic'])

		return redirect(url_for('main.match_results'))
	
	return render_template('filter_plants.html')


# Route: Page 5 - Matching filter results---------------------------------------------#
# define function to retrieve db data


def get_db_plant_filter(light_options):
	plant_list = Plantspecs.query.filter_by(sunlight_need=light_options).all()
	results = plants_schema.dump(plant_list)
	
	return results


@main.route('/match-results')
def match_results():

	# DB query
	filtered_plants = get_db_plant_filter(session['light'])
	print(filtered_plants)
	
	return render_template('match_results.html', 
		filtered_plants = filtered_plants, 
		light = session['light'], 
		water = session['water'], 
		not_toxic = session['not_toxic'], 
		kids_toxic = session['kids_toxic'],
		dogs_toxic = session['dogs_toxic'],
		cats_toxic = session['cats_toxic']
		)