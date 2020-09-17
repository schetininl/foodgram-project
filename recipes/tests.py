from django.test import TestCase, Client


class IndexPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_post(self):
        """Доступна ли главная страница"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
