import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    # print(type(anime_id))
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
        content_recommendations.extend(content_based_recommendations(int(anime_id), anime_data, cosine_sim))

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
            'anime_name': anime_data[anime_data['anime_id'] == anime_id]['name'].iloc[0],
            "image_path": "/anime_images/" + str(anime_id) + ".jpg",
            'hybrid_score': hybrid_score,
            'content_similarity': content_score,
            'predicted_rating': cf_score
        })

    recommendations = sorted(recommendations, key=lambda x: x['hybrid_score'], reverse=True)[:10]
    return recommendations