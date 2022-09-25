import pandas as pd


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
        p = df[(df['prime_genre'] == "News") & df['rating_count_tot']]
        p3 = p[p['rating_count_tot'] == p['rating_count_tot'].max()]
        print(p3)
        p_json = p3.to_json()
        # TODO write to csv, json
        return p_json

    @classmethod
    def top_10_music_book_rating(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") | (df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p.nlargest(10, ['rating_count_tot'])
        print(p3)
        p_json = p3.to_json()
        # TODO write to csv, json
        return p_json

    @classmethod
    def top_10_music_book_citation(cls):
        df = pd.read_csv('static/AppleStore.csv')
        p = df[(df['prime_genre'] == "Music") | (df['prime_genre'] == "Book") & df['rating_count_tot']]
        p3 = p[p['rating_count_tot'] == p['rating_count_tot'].max()]
        print(p)
        print(p3)
        p_json = p3.to_json()
        #TODO write to csv, json
        return p_json


