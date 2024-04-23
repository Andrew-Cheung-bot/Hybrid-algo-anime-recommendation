import uuid
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

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


if __name__ == '__main__':
    app.run()
