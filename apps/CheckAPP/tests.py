from django.test import TestCase
from django.urls import reverse

class OAuthCallbackTest(TestCase):
    def test_oauth_callback(self):
        response = self.client.get(reverse('oauth_callback') + '?code=test_code')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'callback.html')
