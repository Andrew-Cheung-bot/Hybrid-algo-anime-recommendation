import requests
import pandas as pd
import os
import time

# Create a directory for storing downloaded images
if not os.path.exists('anime_images'):
    os.makedirs('anime_images')


# Function to download and save an image
def download_image(image_url, image_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)


# Read anime names from the CSV file
df = pd.read_csv('anime.csv')

# Define the GraphQL query
query = '''
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    title {
      romaji
    }
    coverImage {
      extraLarge
    }
  }
}
'''

url = 'https://graphql.anilist.co'

# Time control setup
requests_per_minute = 80
request_interval = 60 / requests_per_minute  # Calculate delay between requests

Not_found_list = []

# Iterate through the anime names in the CSV
for index, row in df.iterrows():
    anime_name = row['name']
    anime_id = row['anime_id']
    variables = {'id': anime_id}
    response = requests.post(url, json={'query': query, 'variables': variables})
    json_data = response.json()

    if json_data and json_data['data'] and json_data['data']['Media']:
        media = json_data['data']['Media']
        if media['coverImage'] and media['coverImage']['extraLarge']:
            image_url = media['coverImage']['extraLarge']
            image_path = f'anime_images/{anime_id}.jpg'  # Name image file using anime_id
            download_image(image_url, image_path)
            print(f"Downloaded image for {anime_name} with ID {anime_id}")
        else:
            print(f"No image found for {anime_name} with ID {anime_id}")
            Not_found_list.append({"id": anime_id, "name": anime_name})
    else:
        print(f"No data found for {anime_name} with ID {anime_id}")
        Not_found_list.append({"id": anime_id, "name": anime_name})

    time.sleep(request_interval)  # Delay between each request to avoid hitting the API rate limit

with open('Not-found-list.txt', 'w') as file:
    for dictionary in Not_found_list:
        file.write(str(dictionary) + '\n')
