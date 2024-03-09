from asgiref.sync import sync_to_async
from django.shortcuts import render
import asyncio

from import_document.forms import CSVImportForm
from import_document.services import ImportDocumentService


async def import_document_view(request):
    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_csv = sync_to_async(
                ImportDocumentService().import_csv, thread_sensitive=False
            )
            await asyncio.gather(import_csv(form))
            return render(request, "success.html")
    else:
        form = CSVImportForm()
    return render(request, "import.html", {"form": form})
