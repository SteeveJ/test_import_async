from api.resources import ExtendedDetailView, ExtendedListView
from import_document.models import Document


class DocumentDetailView(ExtendedDetailView):
    model = Document
    fields = (
        "folder_number",
        "verling_folder_number",
        "support",
        "ancart",
        "channel",
        "step",
    )
    context_object_name = "document"
    slug_field = "folder_number"
    slug_url_kwarg = "num_doss"
    query_pk_and_slug = False

    def get_queryset(self):
        return Document.objects.filter(folder_number=self.kwargs["num_doss"])


class DocumentListView(ExtendedListView):
    model = Document
    fields = (
        "folder_number",
        "verling_folder_number",
        "support",
        "ancart",
        "channel",
        "step",
    )

    def get_queryset(self):
        return Document.objects.all()
