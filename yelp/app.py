# import necessary libraries
import os
from flask import (Flask,render_template,jsonify,request,redirect,url_for, json, render_template, flash)
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (func, or_, create_engine)
import requests
from config import api_key
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from .mlscript import similarity_model, get_title_from_index, get_index_from_title,print_statement, get_abv_from_index, get_beerstyle_from_index, get_brewery_from_index 

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config.from_object(__name__)
# app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

#################################################
# Maps Setup
#################################################
mapkey = os.environ.get('MAPKEY', '') or "CREATE MAPKEY ENV"

#################################################
# Database Setup
#################################################
import os 
cd = os.getcwd()
# df_5000 = pd.read_csv(cd+"/beer/df500.csv")

from flask_sqlalchemy import SQLAlchemy

#Database Variables
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/yelp.sqlite"

db = SQLAlchemy(app)
from .models import yelpdata
Base = automap_base()
Base.prepare(db.engine, reflect=True)

###############################################
#########Html Routes for Web Server ###########
###############################################
####Landing Page####
@app.route("/")
def index():

    return render_template("index.html")
@app.route("/testing/")
def testing():
    name = []
    city = []
    state = []
    category = []
    latitude = []
    longitude = []
    price = []
    review_count = []
    business_id = []
    rating = []

    def query_search(set_num):
        url = 'https://api.yelp.com/v3/businesses/search'
        headers = {
            'Authorization': 'Bearer {}'.format(api_key),}
        url_params = { #parameters passed to the API
        "term": thing,
        "location": location,
        'offset': offset_num,
        "limit":50
        }

        response = requests.get(url, headers=headers, params=url_params)
        return response.json()

        for offset_num in range(offset):
            try:
            response = query_search(offset_num)
            businesses=response['businesses']
            for x in businesses:
                name.append(x['name'])
                business_id.append(x['id'])
                city.append(x['location']['city'])
                state.append(x['location']['state'])
                latitude.append(x['coordinates']['latitude'])
                longitude.append(x['coordinates']['longitude'])
                review_count.append(x['review_count'])
                rating.append(x['rating'])
                category.append(x['categories'][0]['title'])
                try:
                    price.append(x['price'])
                except KeyError:
                    price.append(0)
    #             print(response)
        except AttributeError:
            print("error at ", offset_num)
        except KeyError:
            print("error at ", offset_num)

    business_df = pd.DataFrame({
    "Business" : name,
    "Business ID": business_id,
    "City": city,
    "State": state,
    "Category": category,
    "Latitude": latitude,
    "Longitude": longitude,
    "Price":price,
    "Reviews": review_count,
    "Rating": rating
    })

    #filters out money column
    business_df['Price'].replace(to_replace=['0'],value=1,inplace=True)
    business_df['Price'].replace(to_replace=['$'],value=1,inplace=True)
    business_df['Price'].replace(to_replace=['$$'],value=2,inplace=True)
    business_df['Price'].replace(to_replace=['$$$'],value=3,inplace=True)
    business_df['Price'].replace(to_replace=['$$$$'],value=4,inplace=True)
    business_df.drop_duplicates()
    business_df

    #drop duplicate values returned
    #export file to csv, Taken from Program Made
    # business_df.to_csv('data/export.csv')

    #just a default return page
    return render_template("index.html")
# @app.route("/scope/")
# def scope():
#     return render_template("scope.html")

# @app.route("/analyst/")
# def analyst():
#     return render_template("analyst.html")

# @app.route("/analysis/")
# def analysis():
#     return render_template("analysis.html")

# @app.route("/sentiment/")
# def sentiment():
#     return render_template("sentiment.html")


#Testing (Route is Hard Coded)
# @app.route('/beer/', defaults={'beer': 'Wachusett Larry'})
# @app.route('/beer/<beer>')
# def beer_input(beer):

#     beerlist = pd.read_csv(cd+"/beer/static/df500.csv")
#     beerlist1 = beerlist['beer_name']

#     df_5000 = pd.read_csv(cd+"/beer/static/df500.csv")
#     count_matrix = CountVectorizer().fit_transform(df_5000["combined_features"])
#     cosine_sim = cosine_similarity(count_matrix)
#     cosine_sim.shape
#     beer_user_likes = (beer)
#     beer_index = get_index_from_title(beer_user_likes)
#     similar_beers = list( enumerate(cosine_sim[beer_index]) )
#     sorted_similar_beers = sorted(similar_beers,key = lambda x:x[1], reverse = True)[1:]
#     i=0
#     beer_dict = []
#     sim_score = []
#     abv_score = []
#     beer = {}
#     beer['beer'] ={}
#     beer['similarity']={}
#     beer['abv']={}
#     beer['brewery']={}
#     case_list=[]
#     # print(f"The top 5 beers similar to {beer_user_likes} are: ")
#     for i in range(len(sorted_similar_beers)):
#         beer_dict.append(get_title_from_index(sorted_similar_beers[i][0]))
#         sim_score.append(sorted_similar_beers[i][1])
#         abv_score.append(get_abv_from_index(sorted_similar_beers[i][0]))
#         case = {'beer': get_title_from_index(sorted_similar_beers[i][0]), 'similarity': (sorted_similar_beers[i][1]), 'abv':(get_abv_from_index(sorted_similar_beers[i][0])), 'style':(get_beerstyle_from_index((sorted_similar_beers[i][0]))), 'brewery':(get_brewery_from_index((sorted_similar_beers[i][0]))) }
#         case_list.append(case)
#         if i>=4:
#             break
#     result = (dict(zip(beer_dict, sim_score)))
#     result2 = dict(zip(beer_dict, abv_score))

#     return render_template("finaltable.html", result=result, result2=result2, beer_user_likes=beer_user_likes, beerlist1=beerlist1, case_list=case_list)

# #Testing (Route is Hard Coded)
# @app.route('/beer/', methods=["POST"])
# def beer_input1():

#     beer = request.form['mybeer']
    
#     beerlist = pd.read_csv(cd+"/beer/static/df500.csv")
#     beerlist1 = beerlist['beer_name']
    

#     df_5000 = pd.read_csv(cd+"/beer/static/df500.csv")
#     count_matrix = CountVectorizer().fit_transform(df_5000["combined_features"])
#     cosine_sim = cosine_similarity(count_matrix)
#     cosine_sim.shape
#     beer_user_likes = (beer)
#     beer_index = get_index_from_title(beer_user_likes)
#     similar_beers = list( enumerate(cosine_sim[beer_index]) )
#     sorted_similar_beers = sorted(similar_beers,key = lambda x:x[1], reverse = True)[1:]
#     i=0
#     beer_dict = []
#     sim_score = []
#     abv_score = []
#     beer = {}
#     beer['beer'] ={}
#     beer['similarity']={}
#     beer['abv']={}
#     case_list=[]
#     # print(f"The top 5 beers similar to {beer_user_likes} are: ")
#     for i in range(len(sorted_similar_beers)):
#         beer_dict.append(get_title_from_index(sorted_similar_beers[i][0]))
#         sim_score.append(sorted_similar_beers[i][1])
#         abv_score.append(get_abv_from_index(sorted_similar_beers[i][0]))
#         case = {'beer': get_title_from_index(sorted_similar_beers[i][0]), 'similarity': (sorted_similar_beers[i][1]), 'abv':(get_abv_from_index(sorted_similar_beers[i][0])), 'style':(get_beerstyle_from_index((sorted_similar_beers[i][0]))), 'brewery':(get_brewery_from_index((sorted_similar_beers[i][0]))) }
#         case_list.append(case)
#         if i>=4:
#             break
#     result = (dict(zip(beer_dict, sim_score)))
#     result2 = dict(zip(beer_dict, abv_score))

#     return render_template("finaltable.html", result=result, result2=result2, beer_user_likes=beer_user_likes, beerlist1=beerlist1, case_list=case_list)


# ##Will return the text that's input
# @app.route('/testroute/')
# def testroute():
#     return '''
# <form method="POST">
#     <input name="text">
#     <input type="submit">
# </form>'''

# @app.route('/testroute/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return ((processed_text))

if __name__ == "__main__":
    app.run()