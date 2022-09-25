import pandas as pd
from sqlalchemy.types import Integer, Text
import re


def get_csv():
    df = pd.read_csv('static/AppleStore.csv')
    df_csv = df.to_csv()
    return df_csv


class storeDb:
    items = [{get_csv()}]

    @classmethod
    def news_rating_count_tot(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "News") & df['rating_count_tot']]
        p3 = p[p['rating_count_tot'] == p['rating_count_tot'].max()]
        p_json = p3.to_json()
        return p_json

    @classmethod
    def top_10_music_book_rating(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") & df['rating_count_tot']]
        p2 = df[(df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p.nlargest(10, ['rating_count_tot'])
        p_json = p3.to_json()
        p2_json = p2.to_json()
        return p_json, p2_json

    @classmethod
    def top_10_music_book_citation(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") & df['rating_count_tot']]
        p2 = df[(df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p.nlargest(10, ['rating_count_tot'])
        p4 = p2.nlargest(10, ['rating_count_tot'])
        p5 = p3['track_name']
        p6 = p4['track_name']
        mus_count = df['track_name'].str.contains(str((x for x in p5)), re.IGNORECASE).sum()
        book_count = df['track_name'].str.contains(str((x for x in p6)), re.IGNORECASE).sum()
        return "Music citation:", str(mus_count), "Book citation:", str(book_count)

    def write_to_csv_and_json(cls):
        from app import eng_exp
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") & df['rating_count_tot']]
        p2 = df[(df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p.nlargest(10, ['rating_count_tot'])
        p4 = p2.nlargest(10, ['rating_count_tot'])
        p5 = p3['track_name']
        p6 = p4['track_name']
        mus_count = df['track_name'].str.contains(str((x for x in p5)), re.IGNORECASE).sum()
        book_count = df['track_name'].str.contains(str((x for x in p6)), re.IGNORECASE).sum()
        d = {'id': p3['id'], 'track_name': p3['track_name'],
             'n_citacoes': mus_count, 'size_bytes': p3['size_bytes'], 'price': p3['price'],
             'prime_genre': p3['prime_genre']}
        d2 = {'id': p4['id'], 'track_name': p4['track_name'],
              'n_citacoes': book_count, 'size_bytes': p4['size_bytes'], 'price': p4['price'],
              'prime_genre': p4['prime_genre']}
        df2 = pd.DataFrame(data=d)
        df3 = pd.DataFrame(data=d2)
        frames = [df2, df3]
        df_concat = pd.concat(frames)
        df_concat.to_json('static/top_10_music_book.json', orient='records', lines=True)
        df_concat.to_csv('static/top_10_music_book.csv', encoding='utf-8', index=False)
        df_concat.to_sql('static/local_db.db', eng_exp, if_exists='replace', index=False, chunksize=500,
                         dtype={
                             "track_name": Text,
                             "n_citacoes": Integer,
                             "size_bytes": Integer,
                             "price": Integer,
                             "prime_genre": Text,
                         }
                         )
        return "Arquivos gerados com sucesso. Verificar pasta static/"
