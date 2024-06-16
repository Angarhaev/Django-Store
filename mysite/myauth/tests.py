from django.test import TestCase
from django.urls import reverse
import json


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:get_cookie'), HTTP_USER_AGENT='test-agent')
        self.assertContains(response, "Cookie value")


class GetJsonViewTesttCase(TestCase):
    def test_get_json(self):
        response = self.client.get(reverse('myauth:get_json'), HTTP_USER_AGENT='test-agent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        expected_data = {'foo': 'bar', 'spam': 'egg'}
        # received_data = json.loads(response.content)
        # self.assertEqual(received_data, expected_data)
        self.assertJSONEqual(response.content, expected_data)



