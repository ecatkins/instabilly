from django.test import TestCase, Client


class TestSomeDjango(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_getrequests(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

