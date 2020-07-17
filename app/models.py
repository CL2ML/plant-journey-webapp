from . import db, ma
from datetime import datetime
from sqlalchemy import inspect

class Plantspecs(db.Model):
	__tablename__ = 'plant_specs'

	id = db.Column(db.Integer, primary_key=True)
	botanical_name = db.Column(db.String(100), index=True, unique=True)  
	common_name = db.Column(db.String(100), index=True, unique=True)
	climate_origin = db.Column(db.String(50))
	sunlight_need = db.Column(db.String(50))
	direct_sunlight = db.Column(db.Boolean())
	water_need = db.Column(db.String(50))
	watering_frequency = db.Column(db.String(50))
	toxic = db.Column(db.Boolean())  
	children = db.Column(db.Boolean()) 
	cats = db.Column(db.Boolean())  
	dogs = db.Column(db.Boolean())  
	blossom_color = db.Column(db.String(50)) 
	fragrance = db.Column(db.String(25))
	best_time_to_plant = db.Column(db.String(50)) 
	size_metric = db.Column(db.String(25))
	mature_size = db.Column(db.String(25))
	repotting_need = db.Column(db.String(100))
	fertilizing_need = db.Column(db.String(355))
	air_humidity = db.Column(db.String(50))
	at_window = db.Column(db.Boolean()) 
	avg_temperature = db.Column(db.String(25)) 
	additional_information = db.Column(db.String())
	experience_need = db.Column(db.String(25)) 
	#created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# Optional solution to return the data as a dict
	def toDict(self):
		return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

	# Data representation for debugging
	def __repr__(self):
		return '<Plantspecs {}>'.format(self.botanical_name)   

# Marshmallow schema to return the data
class PlantSchema(ma.Schema):
    class Meta:
        fields = (
			'botanical_name', 
			'common_name', 
			'climate_origin', 
			'sunlight_need', 
			'direct_sunlight', 
			'water_need', 
			'watering_frequency', 
			'toxic', 
			'children', 
			'cats', 
			'dogs', 
			'blossom_color', 
			'fragrance', 
			'best_time_to_plant', 
			'size_metric', 
			'mature_size', 
			'repotting_need',
			'air_humidity',
			'at_window',
			'avg_temperature',
			'additional_information',
			'experience_need'
			)

