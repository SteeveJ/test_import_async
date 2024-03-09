from django.urls import path

from .document import DocumentDetailView

urlpatterns = [
    path(
        "document/<str:num_doss>/", DocumentDetailView.as_view(), name="document_detail"
    ),
]
