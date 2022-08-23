import json
from django.http import HttpResponse
from invoiceapp.models import Particular


def delete_particulars(request, pk):
    if request.method == 'POST':
        Particular.objects.get(pk=pk).delete()
    return HttpResponse(json.dumps({"message": "successfully deleted"}))

