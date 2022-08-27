'''
Author: Mahesh Kumar
Email: pmaheshkumar139@gmail.com
Date:  26-08-2022
'''

import pickle
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS, cross_origin
import flask_cors as fc
from flask import Response
import os
import pandas as pd
app = Flask(__name__,template_folder='templates',static_folder='templates')

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')
@app.route("/getTopMovies", methods=['POST'])
@cross_origin()
def predictMovie():
    print("Hello")
    if request.json is not None:
        movie = request.json['selectedMovie']
        print(request.json['selectedMovie'])
        try:
            mov, ids = recommend(movie)
            res_zip = [ [m,id] for m,id in zip(mov, ids)]
            df = pd.DataFrame(res_zip, columns =['Movies', 'Id']) 
            data = df.to_json(orient='records')
            re={"data":data,"error":False,"message":"successful"}
            print("RESPONSe",re)
            return jsonify(re)
        except:
             print("Wrong")
    else :
        return Response("Error")
def recommend(movie):
        try:
            recommended_movies = []
            recommended_movies_id=[]
            text_new_df = pickle.load(open('movie_list.pkl','rb'))
            similarity = pickle.load(open('similarity.pkl','rb'))
            print("Hello 1")
            index = text_new_df[text_new_df['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
            for i in distances[1:6]:
                recommended_movies.append(text_new_df.iloc[i[0]].title)
                recommended_movies_id.append(text_new_df.iloc[i[0]].movie_id)
            return recommended_movies,recommended_movies_id
        except ValueError:
            print("Inner Error")
            return ValueError

@app.route("/getMoviesList", methods=['GET'])
@cross_origin()
def getMoviesList():
    movies = pickle.load(open('movie_list.pkl','rb'))
    lists = list(movies['title'])
    df = pd.DataFrame(lists)
    data = df.to_json(orient='records')
    re={"data":lists,"error":False,"message":"successful"}
    print("RESPONSe",df.head(2))
    return jsonify(re)
port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    app.run(debug=True)

