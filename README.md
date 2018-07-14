# foodfight
A Python Flask web app to track food interest in Austin over time from search trends. Now we know if more people are interested in tacos or BBQ at any given time!

The back end uses Python to fetch Google Trends data for the keywords from the user form input.

The front end uses Flask-WTForms, Jinja2 templates, Bootstrap, and Chart.js to visualize the results neatly.

## Setup:
```
$ pip install -r requirements.txt
```
```
$ mv env_example .env
```
```
$ source .env
```
```
$ python app.py
```