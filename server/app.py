import uuid
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import hybridAlgo
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from werkzeug.middleware.proxy_fix import ProxyFix
import json

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# sanity check route


@app.route('/listBooks', methods=['GET'])
def listBooks():
    df = pd.read_csv('anime.csv')
    df_shuffled = df.sample(frac=1)
    data = []
    count = 0

    for index, row in df_shuffled.iterrows():
        if count == 6:
            break
        anime_name = row['name']
        anime_id = row['anime_id']
        genre = row['genre']
        tags_list = genre.split(', ')
        data.append({"anime_name": anime_name,
                    "image_path": "/anime_images/" + str(anime_id) + ".jpg",
                     "genre": tags_list, "anime_id": anime_id})
        count += 1

    return jsonify(data)


@app.route('/listBooksForMaster', methods=['GET'])
def listBooksForMaster():
    df = pd.read_csv('anime.csv')
    data = []

    for id in (339, 32, 30, 971, 249, 270):
        row_data = df[df['anime_id'] == id]
        anime_name = row_data['name'].values[0]
        anime_id = row_data['anime_id'].values[0].item()
        genre = row_data['genre'].values[0]
        tags_list = genre.split(', ')
        data.append({"anime_name": anime_name,
                    "image_path": "/anime_images/" + str(anime_id) + ".jpg",
                     "genre": tags_list, "anime_id": anime_id})
        
    print(data)

    return jsonify(data)


@app.route('/rate', methods=['POST'])
def rate_animes():
    anime_data = pd.read_csv('anime.csv')
    ratings_data = pd.read_csv('rating.csv')

    data = request.json
    user_ratings = json.loads(data['ratings'])
    # print('user_rating', user_ratings)

    # Add new user's ratings to ratings_data
    new_user_id = ratings_data['user_id'].max() + 1
    new_ratings = [{'user_id': new_user_id, 'anime_id': int(anime_id), 'rating': rating} for anime_id, rating in
                   user_ratings.items()]
    # print('new Ratings', new_ratings)
    new_ratings_df = pd.DataFrame(new_ratings)
    ratings_data = pd.concat([ratings_data, new_ratings_df], ignore_index=True)

    # Create dataset and train model
    reader = Reader(rating_scale=(1, 10))
    new_data = Dataset.load_from_df(
        ratings_data[['user_id', 'anime_id', 'rating']], reader)
    trainset_new = new_data.build_full_trainset()
    model = SVD()
    model.fit(trainset_new)

    # Content-based filtering setup
    tfidf = TfidfVectorizer(stop_words='english')
    anime_data['genre'].fillna('', inplace=True)
    tfidf_matrix = tfidf.fit_transform(anime_data['genre'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    recommended_animes = hybridAlgo.hybrid_recommendations(
        new_user_id, user_ratings, model, anime_data, cosine_sim)
    # print(recommended_animes)

    return jsonify(recommended_animes)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
    # if you use gunicorn to deploy on server, run the codes below
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    # app.run()

    # bash command: gunicorn -w 5 -b 0.0.0.0:5001 app:app
