from flask import Flask, render_template,session, redirect, url_for,flash, request
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                    RadioField, SelectField, TextField,
                    TextAreaField, SubmitField)
from wtforms.validators import DataRequired
import pandas as pd
import numpy as np
df = pd.read_csv('data_final.csv')
#df2=pd.read_csv('data_final.csv')

app= Flask(__name__)

@app.route('/')
def index():

    return render_template('right-strain-landing.html')

@app.route('/strainfinder')
def test():

    strains= df['strain_list'].tolist()
    return render_template('right-strain-finder.html', strains= strains)

@app.route('/model', methods= ["POST"])
def jono():

    strain= request.form.get('strain')
    weight= request.form.get('weight')

    print(strain)
    print(weight)

    def distance(row):
        cols = ['Feat0','Feat1','Feat2','Feat3','Feat4','Feat5','Feat6','Feat7']
        return(df[cols]-row[cols]).abs().sum(axis=1)

    df.set_index('strain_list', inplace=True)
    dist= df.apply(distance, axis=1)

    recommendation= dist[strain].nsmallest(4).index.tolist()[1:]

    first_choice= recommendation[0]
    second_choice= recommendation[1]
    third_choice= recommendation[2]

    return render_template('right-strain-finder-results.html', first_choice= first_choice, second_choice=second_choice, third_choice= third_choice)



if __name__=='__main__':
    app.run(debug=True)
