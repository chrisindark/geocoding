import xlrd
import xlwt
import googlemaps

from django.http import HttpResponse
from django.views.generic import FormView
from django.conf import settings

from .forms import GeocodeFileForm


# Create your views here.
class GeocodeCreateView(FormView):
    template_name = 'geocode_form.html'
    form_class = GeocodeFileForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        input_excel = form.cleaned_data['file']
        return self.import_xls(input_excel)

    def import_xls(self, input_excel):
        result = []
        gmaps = googlemaps.Client(settings.GOOGLE_MAPS_API_KEY)

        wb = xlrd.open_workbook(file_contents = input_excel.read())
        for i in range(wb.nsheets):
            ws = wb.sheet_by_index(i)
            for j in range(ws.nrows):
                geocode_result = gmaps.geocode(ws.cell_value(j, 0))
                geocode_location = geocode_result[0]['geometry']['location']
                result.append([ws.cell_value(j, 0), geocode_location])

        return self.export_xls(result)

    def export_xls(self, result):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="geocodes.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Geocodes')

        row_num = 0
        col_headers = ['Address', 'Latitude', 'Longitude']
        for col in range(len(col_headers)):
            ws.write(row_num, col, col_headers[col])

        for row in range(len(result)):
            ws.write(row + 1, 0, result[row][0])
            ws.write(row + 1, 1, result[row][1]['lat'])
            ws.write(row + 1, 2, result[row][1]['lng'])
        wb.save(response)
        return response
