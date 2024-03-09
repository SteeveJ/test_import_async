from django.db import models
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    ETR = "ETR"
    FRA = "FRA"
    CHANNEL_CHOICES = (
        (ETR, "ETR"),
        (FRA, "FRA"),
    )

    folder_number = models.CharField(
        verbose_name=_("folder number"), unique=True, max_length=100
    )
    verling_folder_number = models.CharField(
        max_length=100, verbose_name=_("Verling folder number")
    )
    ancart = models.CharField(max_length=20, verbose_name=_("Ancart"))
    channel = models.CharField(
        max_length=3, choices=CHANNEL_CHOICES, blank=True, verbose_name=_("Channel")
    )
    step = models.CharField(max_length=50, verbose_name=_("Step"))

    def __str__(self):
        return self.folder_number
