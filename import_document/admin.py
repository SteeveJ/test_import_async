from django.contrib import admin
from import_document.models import Document, Support


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "folder_number",
        "verling_folder_number",
        "ancart",
        "channel",
        "step",
    )
    search_fields = (
        "folder_number",
        "verling_folder_number",
        "ancart",
        "channel",
        "step",
    )


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ("folder_number", "verling", "format")
    search_fields = ("folder_number", "verling", "format")
