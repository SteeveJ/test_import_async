import json

from django.test import TestCase
from django.urls import reverse
from snapshottest import TestCase as TestCaseSnapshot

from tests.factories import DocumentFactory, SupportFactory


class TestDocumentView(TestCase, TestCaseSnapshot):
    @classmethod
    def setUpTestData(cls):
        DocumentFactory.create_batch(300)
        document = DocumentFactory(
            folder_number="DD237051",
            verling_folder_number="DD237051",
            ancart="LNEN50289-1-3",
            channel="ETR",
            step="60.62",
        )
        SupportFactory(
            folder_number=document,
            verling="E",
            format="PDFC",
        )
        SupportFactory(
            folder_number=document,
            verling="F",
            format="XML",
        )
        cls.document = document

    def test_document_list(self):
        url = reverse("document_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["page_num"], 0)
        self.assertEqual(response_json["page_size"], 100)
        self.assertEqual(response_json["total_size"], 301)
        self.assertMatchSnapshot(response_json)

    def test_document_pagination(self):
        url = reverse("document_list")
        response = self.client.get(url, {"page_num": 2})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["page_num"], 2)
        self.assertMatchSnapshot(response_json)

    def test_page_size(self):
        url = reverse("document_list")
        response = self.client.get(url, {"page_size": 50})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["page_size"], 50)
        self.assertMatchSnapshot(response_json)

    def test_document_detail(self):
        url = reverse(
            "document_detail", kwargs={"num_doss": self.document.folder_number}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["folder_number"], self.document.folder_number)
        self.assertEqual(
            response_json["verling_folder_number"], self.document.verling_folder_number
        )
        self.assertEqual(response_json["ancart"], self.document.ancart)
        self.assertEqual(response_json["channel"], self.document.channel)
        self.assertEqual(response_json["step"], self.document.step)
        self.assertMatchSnapshot(response_json)
