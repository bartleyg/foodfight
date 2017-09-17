from pytrends.request import TrendReq
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
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
            flash('Error: All the form fields are required. ')
 
    # get google trends data
    pytrend.build_payload(kw_list=[food1, food2], timeframe='now 1-H', geo='US-TX-635')
    tacos_bbq_df = pytrend.interest_over_time()

    # add hover tool
    hovertool = HoverTool(tooltips='@y{0}')

    # create a new plot with a datetime axis type
    p = figure(plot_width=800, plot_height=250, x_axis_type="datetime",
                toolbar_location="above", tools=[hovertool],
                responsive=True, outline_line_color="#666666")
    p.yaxis.axis_label = "Interest"
    p.xaxis.axis_label = "Time"
    p.toolbar.logo = None

    # plot 2 data lines
    p.line(tacos_bbq_df.index, tacos_bbq_df[food1], legend=list(tacos_bbq_df)[0],
                color='blue', alpha=0.8, line_width=3)
    p.line(tacos_bbq_df.index, tacos_bbq_df[food2], legend=list(tacos_bbq_df)[1],
                color='red', alpha=0.8, line_width=3)

    # make the javascript and html div
    script, div = components(p)

    return render_template("trends_chart.html", form=form, the_div=div, the_script=script,
                            food1=food1, food2=food2)


if __name__ == "__main__":
    # launch Flask webserver on default host port
    app.run()

