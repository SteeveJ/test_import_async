from django.test import TestCase
from django.urls import reverse


class TestDocumentView(TestCase):
    def test_document_list(self):
        url = reverse("document_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_document_detail(self):
        url = reverse("document_detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
