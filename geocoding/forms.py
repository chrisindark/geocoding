from django import forms


ALLOWED_FILE_TYPES = ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel')


class GeocodeFileForm(forms.Form):
    file = forms.FileField(label='Select a file')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        file_type = self.get_file_type(file)
        return file

    def get_file_type(self, file):
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise forms.ValidationError('File type should be of xls/xlsx format')
