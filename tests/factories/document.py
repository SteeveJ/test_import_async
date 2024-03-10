from factory.django import DjangoModelFactory
import factory

from import_document.models import Document


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    folder_number = factory.Sequence(lambda n: "DD%s" % n)
    verling_folder_number = "verling_folder_number"
    ancart = "ancar"
    channel = "ETR"
    step = "step"
