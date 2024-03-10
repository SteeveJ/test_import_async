from django.urls import path

from .document import DocumentDetailView, DocumentListView

urlpatterns = [
    path(
        "documents/<str:num_doss>/",
        DocumentDetailView.as_view(),
        name="document_detail",
    ),
    path("documents/", DocumentListView.as_view(), name="document_list"),
]
