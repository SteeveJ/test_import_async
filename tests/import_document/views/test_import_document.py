import os
from django.test import TestCase
from django.urls import reverse

from import_document.constants import ONLY_CSV_FILE_ALLOWED
from import_document.models import Document, Support


class TestImportDocumentView(TestCase):
    def SetUp(self):
        pass

    def test_import_document(self):
        url = reverse("import_document")
        # load csv
        file_name = "/data/test.csv"
        base_path = os.path.dirname(os.path.realpath(__file__))

        with open(base_path + file_name, "rb") as f:
            response = self.client.post(url, {"csv_file": f})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 37895)
        self.assertEqual(Support.objects.count(), 49974)

    def test_import_document_invalid(self):
        url = reverse("import_document")
        # load csv
        file_name = "/data/test_invalid.csv"
        base_path = os.path.dirname(os.path.realpath(__file__))

        with open(base_path + file_name, "rb") as f:
            response = self.client.post(url, {"csv_file": f})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Support.objects.count(), 0)

    def test_import_document_empty(self):
        url = reverse("import_document")
        # load csv
        file_name = "/data/test_empty.csv"
        base_path = os.path.dirname(os.path.realpath(__file__))

        with open(base_path + file_name, "rb") as f:
            response = self.client.post(url, {"csv_file": f})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Support.objects.count(), 0)

    def test_import_document_no_file(self):
        url = reverse("import_document")
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Support.objects.count(), 0)

    def test_import_document_invalid_file(self):
        url = reverse("import_document")
        # load csv
        file_name = "/data/test_invalid.txt"
        base_path = os.path.dirname(os.path.realpath(__file__))

        with open(base_path + file_name, "rb") as f:
            response = self.client.post(url, {"csv_file": f})

        self.assertContains(response, ONLY_CSV_FILE_ALLOWED, html=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Document.objects.count(), 0)
        self.assertEqual(Support.objects.count(), 0)
