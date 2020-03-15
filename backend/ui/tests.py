from django.test import TestCase
from django.urls import reverse


class UrlTests(TestCase):
    def test_svelte_home(self):
        response = self.client.get(reverse("ui:svelte_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ui/home.html")
