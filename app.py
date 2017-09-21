from pytrends.request import TrendReq
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

# App config.
DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d661f27d881f27567d441f2b6176a'

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

class ReusableForm(Form):
    food1 = TextField('Food 1:', validators=[DataRequired()])
    food2 = TextField('Food 2:', validators=[DataRequired()])

@app.route("/", methods=['GET', 'POST'])
def trends_chart():
    # get user input from form
    form = ReusableForm(request.form)
    print(form.errors)

    # default for when GET first run no input
    food1 = 'tacos'
    food2 = 'bbq'

    # if data input from form
    if request.method == 'POST':
        food1 = request.form['food1']
        food2 = request.form['food2']
        print(food1, " ", food2)
        if form.validate():
            # Save the comment here.
            flash('Analyzing ' + food1 + ' vs ' + food2)
        else:
            flash('Error: All the form fields are required.')
 
    # get google trends data past 24 hours
    pytrend.build_payload(kw_list=[food1, food2], timeframe='now 1-d', geo='US-TX-635')
    food_24h_df = pytrend.interest_over_time()

    # time - y axis
    time_24h = food_24h_df.index
    # interest values - x axis
    food1_24h = food_24h_df[food1]
    food2_24h = food_24h_df[food2]

    # get google trends data past week
    pytrend.build_payload(kw_list=[food1, food2], timeframe='now 7-d', geo='US-TX-635')
    food_7d_df = pytrend.interest_over_time()

    # time - y axis
    time_7d = food_7d_df.index
    # interest values - x axis
    food1_7d = food_7d_df[food1]
    food2_7d = food_7d_df[food2]
   
    return render_template("trends_chart.html", form=form, food1=food1, food2=food2,
                    time_24h=time_24h, food1_24h=food1_24h, food2_24h=food2_24h,
                    time_7d=time_7d, food1_7d=food1_7d, food2_7d=food2_7d
                    )


if __name__ == "__main__":
    # launch Flask webserver on default host port
    app.run()

