import json

import pandas as pd
from flask import flash, request, render_template
from sqlalchemy.types import Integer, Text, String, DateTime


def get_csv():
    df = pd.read_csv('static/AppleStore.csv')
    df_csv = df.to_csv()
    return df_csv


class storeDb:
    items = [{get_csv()}]

    @classmethod
    def adicionar(cls, item):
        cls.items.append(item)
        return True

    @classmethod
    def obter(cls, id=None):
        if id:
            return next(filter(lambda x: x['id'] == id, cls.items), {})
        return cls.items

    @classmethod
    def remover(cls, id):
        # cls.items = [for item in cls.items if item['id'] != id]
        cls.items = list(filter(lambda x: x['id'] != id, cls.items))
        return {"mensagem": f"id {id} deletado com sucesso"}

    @classmethod
    def alterar(cls, id, novo_item: dict):
        item = next(filter(lambda x: x['id'] == id, cls.items), {})
        index = cls.items.index(item)

        if novo_item.get('nome'):
            item['nome'] = novo_item.get('nome')

        if novo_item.get('endereco'):
            item['endereco'] = novo_item.get('endereco')

        cls.items[index] = item
        return item

    @classmethod
    def news_rating_count_tot(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p[p['rating_count_tot'] == p['rating_count_tot'].max()]
        # print(p3)
        p_json = p3.to_json()
        return p_json

    @classmethod
    def top_10_music_book_rating(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") | (df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p.nlargest(10, ['rating_count_tot'])
        p_json = p3.to_json()
        return p_json

    @classmethod
    def top_10_music_book_citation(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") | (df['prime_genre'] == "Book") & df['rating_count_tot']]
        # TODO citation
        p3 = p.nlargest(10, ['rating_count_tot'])
        p4 = ""
        # print(p3)
        p_json = p3.to_json()
        return p_json

    def write_to_csv_and_json(cls):
        from app import eng_exp
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") | (df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p.nlargest(10, ['rating_count_tot'])
        # TODO n_citacoes
        d = {'id': p3['id'], 'track_name': p3['track_name'],
             'n_citacoes': "", 'size_bytes': p3['size_bytes'], 'price': p3['price'],
             'prime_genre': p3['prime_genre']}
        df2 = pd.DataFrame(data=d)
        df2.to_json('static/top_10_music_book.json', orient='records', lines=True)
        df2.to_csv('static/top_10_music_book.csv', encoding='utf-8', index=False)
        df2.to_sql('static/local_db.db', eng_exp, if_exists='replace', index=False, chunksize=500,
                   dtype={
                       "track_name": Text,
                       "n_citacoes": Integer,
                       "size_bytes": Integer,
                       "price": Integer,
                       "prime_genre": Text,
                   }
                   )

        flash('Record was successfully added')
        return "Arquivos gerados com sucesso. Verificar pasta static/"
