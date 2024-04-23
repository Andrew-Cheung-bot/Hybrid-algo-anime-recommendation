# How to run  
## 1. Download image dataset
- This repo has already downloaded *Anime Recommendations Database*<sup><a href="#ref1">1</a></sup> from Kaggle
- But still need to download images dataset for running
    - Download link : [anime_images](https://drive.google.com/file/d/1m_zUt278LqlSNLmq9QsRo_jYgQmikmh9/view?usp=sharing)
    - move it to `./client/public/` folder below
## 2. Back-end server (Flask)
```bash
$ cd server
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ flask run --port=5001 --debug
```
> Besides, you can use Anaconda/miniconda to create virtual Environment.
## 3. Front-end server (Vue3.js)
```bash
$ cd client
$ npm install
$ npm run dev
```
## 4. Website
- [localhost:3000](http://localhost:3000) -> front-end
- [localhost:5001](http://localhost:5001) -> back-end
## Reference
<p id="ref1">[1]“Anime Recommendations Database,” Kaggle, Dec. 21, 2016. https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database</p>