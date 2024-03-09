from asgiref.sync import sync_to_async
from django.db import transaction
from setuptools.command.easy_install import update_dist_caches

from import_document.forms import CSVImportForm
from import_document.models import Document, Support


class ImportDocumentService:
    """
    Service to import CSV file to Document and Support models
    """

    def _batch_udpate_documents(self, documents: list[Document]) -> list[Document]:
        return Document.objects.bulk_create(
            objs=documents,
            update_fields=[
                "folder_number",
                "verling_folder_number",
                "ancart",
                "channel",
                "step",
            ],
            update_conflicts=True,
            unique_fields=["folder_number"],
            batch_size=1000,
        )

    def _batch_create_supports(
        self, supports: dict[str, list[dict]], documents: list[Document]
    ) -> list[Support]:
        new_support: list[Support] = list()
        for document in documents:
            for support in supports[document.folder_number]:
                new_support.append(
                    Support(
                        folder_number=document,
                        verling=support["verling"],
                        format=support["format"],
                    )
                )

        return Support.objects.bulk_create(
            objs=new_support,
            update_fields=["verling", "format", "folder_number"],
            batch_size=1000,
        )

    def import_csv(self, form: CSVImportForm) -> None:
        csv_file = form.cleaned_data["csv_file"]
        documents: dict[str, Document] = dict()
        supports: dict[str, list[dict]] = dict()

        for line in csv_file:
            decoded_line = line.decode("utf-8")
            try:
                (
                    folder_number,
                    verling_folder_number,
                    ancart,
                    channel,
                    step,
                    verling,
                    format,
                ) = decoded_line.split(";")
            except ValueError:
                continue

            if "NUMDOS" in folder_number:
                continue

            if folder_number not in documents:
                documents[folder_number] = Document(
                    folder_number=folder_number,
                    verling_folder_number=verling_folder_number,
                    ancart=ancart,
                    channel=channel,
                    step=step,
                )
                supports[folder_number] = list()

            supports[folder_number].append(
                {
                    "folder_number": folder_number,
                    "verling": verling,
                    "format": format,
                }
            )

        if len(documents) == 0:
            return

        with transaction.atomic():
            new_documents = self._batch_udpate_documents(list(documents.values()))
            self._batch_create_supports(supports, new_documents)
