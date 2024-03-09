# Generated by Django 5.0.3 on 2024-03-09 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "folder_number",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="folder number"
                    ),
                ),
                (
                    "verling_folder_number",
                    models.CharField(
                        max_length=100, verbose_name="Verling folder number"
                    ),
                ),
                ("ancart", models.CharField(max_length=20, verbose_name="Ancart")),
                (
                    "channel",
                    models.CharField(
                        blank=True,
                        choices=[("ETR", "ETR"), ("FRA", "FRA")],
                        max_length=3,
                        verbose_name="Channel",
                    ),
                ),
                ("step", models.CharField(max_length=50, verbose_name="Step")),
            ],
        ),
        migrations.CreateModel(
            name="Support",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "verling",
                    models.CharField(
                        blank=True,
                        choices=[("E", "E"), ("F", "F"), ("E/F", "E/F")],
                        max_length=3,
                        verbose_name="Verling",
                    ),
                ),
                (
                    "format",
                    models.CharField(
                        blank=True,
                        choices=[("PDFC", "PDFC"), ("PDFI", "PDFI"), ("XML", "XML")],
                        max_length=15,
                        verbose_name="Format",
                    ),
                ),
                (
                    "folder_number",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="support_folder_number",
                        to="import_document.document",
                        verbose_name="Verling document number",
                    ),
                ),
            ],
        ),
    ]
