from . import db
from datetime import datetime

class Plantspecs(db.Model):
	__tablename__ = 'plant_specs'

	id = db.Column(db.Integer, primary_key=True)
	botanical_name = db.Column(db.String(100), index=True, unique=True)  
	common_name = db.Column(db.String(100), index=True, unique=True)
	light_requirements = db.Column(db.String(50))
	water_requirements  = db.Column(db.String(50))
	additional_characteristics = db.Column(db.String())
	blossom_color = db.Column(db.String(50)) 
	best_time_to_plant = db.Column(db.String(50)) 
	fragrance = db.Column(db.String(25))
	mature_size = db.Column(db.String(25))
	fertilizing_need = db.Column(db.String(355))
	air_humidity = db.Column(db.String(50))
	direct_sunlight = db.Column(db.Boolean())
	at_window = db.Column(db.Boolean()) 
	avg_temperature = db.Column(db.String(25)) 
	toxic = db.Column(db.Boolean())  
	cats = db.Column(db.Boolean())  
	dogs = db.Column(db.Boolean())  
	children = db.Column(db.Boolean())  
	climate_origin = db.Column(db.String(50))  
	repotting_need = db.Column(db.String(100))
	created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# Data representation for debugging
	def __repr__(self):
		return '<Plantspecs {}>'.format(self.botanical_name)   