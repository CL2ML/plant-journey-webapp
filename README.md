# Prototype for the Plant Journey App

Using the Flask Framework for the Backend.
## 


[PlantJourney App](plantjourney-proto.herokuapp.com)



## Architecture

PlantJourney Web app <-> Image recognition API server

__Business logic:__

The user can upload an image from a unknown plant which will recognized by a deep learning model. After the image upload, the web app makes an API request and sends the file to the image recognition API. The web app receives the recognized plant class in return. The plant class will then be used to query the database for more information on the recognized plant (e.g. water and light requirements). The     


__PlantJourney Web app:__

- Backend:
    - Flask web app
    - Gunicorn app server (used by heroku)
    - Heroku.com Hosting Server
    - PostgreSQL database by heroku 
- Frontend: plain JavaScript, HTML, CSS as well as Jinja

__PlantJourney image recognition API server:__

The image recognition API was also built with Flask and is hosted on heroku.com. The image recognition model [ResNet34](https://docs.fast.ai/vision.models.html) has been trained with [fast.ai](https://www.fast.ai/). Fast.ai is also used in production - yes, it works just fine! If you want find out more about the image recognition API, have a look at this [github repo](https://github.com/CM2ML/plant-recognition-api). 

## Credits

We used a lot of resources from authors on the web to whom we are very grateful for their explanations. 

We warmly recommend the book ["Flask Web Development" by Miguel Grinberg](https://www.flaskbook.com/) which opened the door into a new world. Also, the web lesson [Flask by Example – Project Setup](https://realpython.com/flask-by-example-part-1-project-setup/) by realpython.com was very helpful.

We would like to give special credits for the following authors and sources across topics that have been very helpful: 

[flask-by-example-part-1-project-setup](https://realpython.com/flask-by-example-part-1-project-setup/): Quick an basic set up with Heroku 

[Flask Mega Tutorial - Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure): App structure

[Github repo for Miguel Grinberg Book "Flask Web Development, 2nd Edition"](https://github.com/miguelgrinberg/flasky): Comprehensive overview

[tutorial flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/): Project layout

[structure-of-a-flask-project](https://lepture.com/en/2018/structure-of-a-flask-project): Nice example of a real project

[realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/): Postgres Database for Flask

[techwithtim.net/tutorials/flask/sessions](https://techwithtim.net/tutorials/flask/sessions/): Use session data to move variable content via redirect

## License

This project is licensed under the terms of the Boost Software License 1.0.

If you want to get in touch with us, feel free to write us a [mail](plantjourney.app@gmail.com).