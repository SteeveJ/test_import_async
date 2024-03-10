from factory.django import DjangoModelFactory

from import_document.models import Support


class SupportFactory(DjangoModelFactory):
    class Meta:
        model = Support

    verling = "E"
    format = "PDFC"
