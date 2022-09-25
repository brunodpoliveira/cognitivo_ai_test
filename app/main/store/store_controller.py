from flask_restplus import Resource, Namespace, fields
from app.main.store.store_db import storeDb
from flask import Flask, request, send_file,render_template
import os
import csv
import pandas as pd

api = Namespace('Store', description='Maintenance of store data')
modelo = api.model('StoreModel', {
    'id': fields.Integer,
    'track_name': fields.String,
    'n_citacoes': fields.Integer,
    'size_bytes': fields.Integer,
    'price': fields.Integer,
    'prime_genre': fields.String,

})


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
class rating_count_tot(Resource):
    def get(self):
        return storeDb.top_10_music_book_rating(), 200

"""
@api.route('/top_10_music_book_citation')
class rating_count_tot(Resource):
    def get(self):
        return storeDb.top_10_music_book_citation(), 200
"""

@api.route('/')
class storeController(Resource):
    @api.response(200, "success")
    def get(self):
        return storeDb.obter(), 200

    @api.expect(modelo)
    def post(self):
        return storeDb.adicionar(request.json), 201
