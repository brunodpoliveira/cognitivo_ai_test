from flask_restplus import Resource, Namespace
from app.main.store.store_db import storeDb
import pandas as pd

api = Namespace('Store', description='Maintenance of store data')


@api.route('/process_csv')
class process_csv(Resource):
    def get(self):
        df = pd.read_csv('static/AppleStore.csv')
        df_json = df.to_json()
        return df_json


@api.route('/max_value_news_rating_count_tot')
class rating_count_tot(Resource):
    def get(self):
        return storeDb.news_rating_count_tot(), 200


@api.route('/top_10_music_book_rating')
class top_10_music_book_rating(Resource):
    def get(self):
        return storeDb.top_10_music_book_rating(), 200


@api.route('/top_10_music_book_citation')
class top_10_music_book_citation(Resource):
    def get(self):
        return storeDb.top_10_music_book_citation(), 200


@api.route('/write_to_csv_and_json')
class write_to_csv_and_json(Resource):
    def post(self):
        return storeDb.write_to_csv_and_json(self), 200
