from django.core.files.uploadedfile import UploadedFile
from django.forms import forms
from django.utils.translation import gettext_lazy as _

from import_document.constants import ONLY_CSV_FILE_ALLOWED


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label=_("Select a CSV file"))

    def __init__(self, *args, **kwargs):
        super(CSVImportForm, self).__init__(*args, **kwargs)
        self.fields["csv_file"].widget.attrs.update({"class": "border p-2 w-full"})
        self.fields["csv_file"].widget.attrs.update({"accept": ".csv"})

    def clean_csv_file(self) -> UploadedFile:
        csv_file = self.cleaned_data["csv_file"]
        if not csv_file.name.endswith(".csv"):
            raise forms.ValidationError(ONLY_CSV_FILE_ALLOWED)
        return csv_file
