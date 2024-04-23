## How to run  
### 1. Download image dataset
- Download: [anime_images](https://drive.google.com/file/d/1m_zUt278LqlSNLmq9QsRo_jYgQmikmh9/view?usp=sharing)
- move it to `./client/public/` folder below
### 2. Back-end server (Flask)
```bash
$ cd server
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ flask run --port=5001 --debug
```
> Besides, you can use Anaconda/miniconda to create virtual Environment.
### 3. Front-end server (Vue3.js)
```bash
$ cd client
$ npm install
$ npm run dev
```
### 4. Website
- [localhost:3000/](localhost:3000) -> front-end
- [localhost:5001/](localhost:5001) -> back-end