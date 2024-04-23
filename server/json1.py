from flask import Flask, request, jsonify
import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data

anime_data = pd.read_csv('anime.csv')
ratings_data = pd.read_csv('rating.csv')


@app.route('/rate', methods=['POST'])
def rate_animes():
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

    recommended_animes = hybrid_recommendations(new_user_id, user_ratings, model, anime_data, cosine_sim)

    return jsonify(recommended_animes)


def calculate_weights(user_ratings):
    ratings = np.array(list(user_ratings.values()))
    mean_rating = np.mean(ratings)
    std_rating = np.std(ratings)

    if mean_rating >= 7:
        content_weight = 0.7
        collaborative_weight = 0.3
    else:
        content_weight = 0.3
        collaborative_weight = 0.7

    if std_rating > 2:
        collaborative_weight += 0.1
        content_weight -= 0.1

    return content_weight, collaborative_weight

def content_based_recommendations(anime_id, anime_data, cosine_sim):
    idx = anime_data.index[anime_data['anime_id'] == anime_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    anime_indices = [i[0] for i in sim_scores]
    return anime_data['anime_id'].iloc[anime_indices].tolist()


def hybrid_recommendations(new_user_id, user_ratings, model, anime_data, cosine_sim):
    content_weight, collaborative_weight = calculate_weights(user_ratings)

    content_recommendations = []
    for anime_id in user_ratings.keys():
        content_recommendations.extend(content_based_recommendations(anime_id, anime_data, cosine_sim))

    cf_predictions = []
    content_scores = {}
    for anime_id in set(content_recommendations):
        prediction = model.predict(new_user_id, anime_id).est
        cf_predictions.append((anime_id, prediction))
        content_scores[anime_id] = content_recommendations.count(anime_id) / len(content_recommendations)

    recommendations = []
    for anime_id, cf_score in cf_predictions:
        content_score = content_scores.get(anime_id, 0)
        hybrid_score = content_weight * content_score + collaborative_weight * cf_score
        recommendations.append({
            'anime_id': anime_id,
            'name': anime_data[anime_data['anime_id'] == anime_id]['name'].iloc[0],
            'hybrid_score': hybrid_score,
            'content_similarity': content_score,
            'predicted_rating': cf_score
        })

    recommendations = sorted(recommendations, key=lambda x: x['hybrid_score'], reverse=True)[:10]
    return recommendations


if __name__ == '__main__':
    app.run(debug=True)
