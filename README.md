# How to run  
## 1. Download image dataset
- This repo has already downloaded *Anime Recommendations Database*<sup><a href="#ref1">1</a></sup> from Kaggle
- But still need to download images dataset for running
    - Download link : [anime_images](https://drive.google.com/file/d/1m_zUt278LqlSNLmq9QsRo_jYgQmikmh9/view?usp=sharing).
    - Create a new folder named "anime_images" below `./client/public/`. 
    - Move *anime_images.zip* to `./client/public/anime_images` and unzip.
## 2. Back-end server (Flask)
```bash
# Anaconda Powershell Prompt
$ cd server
$ conda create --prefix ./.conda python=3.11 --file requirements.txt
$ conda activate ./.conda  
(env)$ conda install -c conda-forge scikit-surprise
(env)$ flask run --port=5001 --debug
```
> If you use `pip` to install scikit-surprise, you may encounter an error that requires Microsoft Visual C++ build tools 14.0 or higher version.  
>
> This hybrid algorithm needs at least 2GB RAM to run, otherwise Flask would crash.
## 3. Front-end server (Vue3.js)
```bash
$ cd client
$ npm install
$ npm run dev
```
> Please ensure that your [Node.js](https://nodejs.org/en/download) version is higher than `v18.20.2(LTS)`.  
## 4. Deployment
- Front-end: [localhost:3000](http://localhost:3000)
- Back-end: [localhost:5001](http://localhost:5001)
## Reference
<p id="ref1">[1]“Anime Recommendations Database,” Kaggle, Dec. 21, 2016. https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database</p>
