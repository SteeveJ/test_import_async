from django.urls import path

from import_document.views import import_document_view, SuccessView

urlpatterns = [
    path("import/", import_document_view, name="import_document"),
    path("import/success/", SuccessView.as_view(), name="success"),
]
