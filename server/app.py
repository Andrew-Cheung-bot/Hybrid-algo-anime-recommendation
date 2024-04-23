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

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

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
        print('test',anime_name)
        data.append({"anime_name": anime_name,
                    "image_path": "/anime_images/" + str(anime_id) + ".jpg"})
        count += 1

    return jsonify(data)

@app.route('/rate', methods=['POST'])
def rate_animes():
    anime_data = pd.read_csv('anime.csv')
    ratings_data = pd.read_csv('rating.csv')

    data = request.json
    user_ratings = data['ratings']

    # Load data for each request to ensure thread safety
    anime_data = pd.read_csv('anime.csv')
    ratings_data = pd.read_csv('rating.csv')

    # Add new user's ratings to ratings_data
    new_user_id = ratings_data['user_id'].max() + 1
    new_ratings = [{'user_id': new_user_id, 'anime_id': anime_id, 'rating': rating} for anime_id, rating in
                   user_ratings.items()]
    new_ratings_df = pd.DataFrame(new_ratings)
    ratings_data = pd.concat([ratings_data, new_ratings_df], ignore_index=True)

    # Create dataset and train model
    reader = Reader(rating_scale=(1, 10))
    new_data = Dataset.load_from_df(ratings_data[['user_id', 'anime_id', 'rating']], reader)
    trainset_new = new_data.build_full_trainset()
    model = SVD()
    model.fit(trainset_new)

    # Content-based filtering setup
    tfidf = TfidfVectorizer(stop_words='english')
    anime_data['genre'].fillna('', inplace=True)
    tfidf_matrix = tfidf.fit_transform(anime_data['genre'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    recommended_animes = hybridAlgo.hybrid_recommendations(new_user_id, user_ratings, model, anime_data, cosine_sim)

    return jsonify(recommended_animes)


if __name__ == '__main__':
    app.run()
