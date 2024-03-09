from django.db import models
from django.utils.translation import gettext_lazy as _


class Support(models.Model):
    E = "E"
    F = "F"
    E_F = "E/F"
    PDFC = "PDFC"
    PDFI = "PDFI"
    XML = "XML"

    VERLING_CHOICES = (
        (E, "E"),
        (F, "F"),
        (E_F, "E/F"),
    )
    FORMAT_CHOICES = (
        (PDFC, "PDFC"),
        (PDFI, "PDFI"),
        (XML, "XML"),
    )

    folder_number = models.ForeignKey(
        "import_document.Document",
        on_delete=models.CASCADE,
        related_name="support_folder_number",
        verbose_name=_("Verling document number"),
    )
    verling = models.CharField(
        max_length=3, choices=VERLING_CHOICES, blank=True, verbose_name=_("Verling")
    )
    format = models.CharField(
        max_length=15, choices=FORMAT_CHOICES, blank=True, verbose_name=_("Format")
    )

    def __str__(self):
        return f"{self.folder_number.folder_number} - {self.verling} - {self.format}"
