import pandas as pd
from pandas import DataFrame
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

anime_data = pd.read_csv('anime.csv')
ratings_data = pd.read_csv('rating.csv')

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(ratings_data[['user_id', 'anime_id', 'rating']], reader)
trainset = data.build_full_trainset()

sample_animes = anime_data.sample(10)
print("Please rate the following animes (rate from 1 to 10):")
user_ratings = {}
for index, row in sample_animes.iterrows():
    print(f"Anime ID: {row['anime_id']}, Name: {row['name']}, Genre: {row['genre']}, Type: {row['type']}")
    user_rating = float(input("Your rating: "))
    user_ratings[row['anime_id']] = user_rating

new_user_id = ratings_data['user_id'].max() + 1

new_ratings = []
for anime_id, rating in user_ratings.items():
    new_ratings.append({'user_id': new_user_id, 'anime_id': anime_id, 'rating': rating})

new_ratings_df = DataFrame(new_ratings)
ratings_data = pd.concat([ratings_data, new_ratings_df], ignore_index=True)
new_data = Dataset.load_from_df(ratings_data[['user_id', 'anime_id', 'rating']], reader)
trainset_new = new_data.build_full_trainset()
model = SVD()
model.fit(trainset_new)

tfidf = TfidfVectorizer(stop_words='english')
anime_data['genre'].fillna('', inplace=True)  # 确保没有空的字段
tfidf_matrix = tfidf.fit_transform(anime_data['genre'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def content_based_recommendations(anime_id):
    idx = anime_data.index[anime_data['anime_id'] == anime_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    anime_indices = [i[0] for i in sim_scores]
    return anime_data['anime_id'].iloc[anime_indices].tolist()


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


def hybrid_recommendations(new_user_id, user_ratings):
    content_weight, collaborative_weight = calculate_weights(user_ratings)

    content_recommendations = []
    for anime_id in user_ratings.keys():
        content_recommendations.extend(content_based_recommendations(anime_id))

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
        explanations = {
            'content_similarity': content_score,
            'predicted_rating': cf_score,
            'hybrid_score': hybrid_score
        }
        recommendations.append((anime_id, hybrid_score, explanations))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]
    return [(anime_id, anime_data[anime_data['anime_id'] == anime_id]['name'].iloc[0], score, exp['content_similarity'], exp['predicted_rating']) for anime_id, score, exp in recommendations]

recommended_animes = hybrid_recommendations(new_user_id, user_ratings)
print("Recommended Animes based on your ratings:")
for anime_id, name, score, content_sim, pred_rating in recommended_animes:
    print(f"Anime ID: {anime_id}, Name: {name}, Predicted Hybrid Rating: {score:.2f}")
    print(f"  Content Similarity Score: {content_sim:.2f} (This score measures how similar the genres and themes of this anime are to those of the animes you rated highly.)")
    print(f"  Collaborative Filtering Prediction: {pred_rating:.2f} (This is the predicted rating based on other similar users' ratings for this anime. Higher scores indicate that users with similar tastes and preferences rated this anime highly.)")
    print()
