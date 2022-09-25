from app.test.test_base import BaseTestCase


class StoreTest(BaseTestCase):
    def test_store_respondendo(self):
        response = self.client.get('/process_csv/get')
        self.assert200(response)
