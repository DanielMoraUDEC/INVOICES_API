
import json
import django
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Invoice

# Create your views here.
class InvoiceView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, id=0):
        if id == 0:
            invoices = list(Invoice.objects.values())
            datos = {'message':'success','invoices':invoices} if len(invoices)>0 else {'message':'Invoices not found...'}
            return JsonResponse(datos)
        else :
            invoice = list(Invoice.objects.filter(id=id).values())
            datos = {'message':'success','invoices':invoice[0]} if len(invoice)>0 else {'message':'Invoice not found...'}
            return JsonResponse(datos)

    def post(self,request):
        print(request.body)
        jd = json.loads(request.body)
        Invoice.objects.create(
            userid = jd['userid'],
            itemid = jd['itemid'],
            unitprice = jd['unitprice'],
            quantity = jd ['quantity'],
            invoicetotal = float(jd['unitprice']) * float(jd['quantity'])
        )
        datos = {'message': 'success'}
        return JsonResponse(datos)

    def put(self,request, id):
        jd = json.loads(request.body)
        invoice = list(Invoice.objects.filter(id=id).values())
        if len(invoice) > 0:
            invoice = Invoice.objects.get(id=id)
            invoice.userid = jd['userid']
            invoice.itemid = jd['itemid']
            invoice.unitprice = jd['unitprice']
            invoice.quantity = jd['quantity']
            invoice.invoicetotal = float(jd['unitprice']) * float(jd['quantity'])
            invoice.save()
            datos = {'message': 'success'}
        else :
            datos = {'message': 'Invoice not found...'}

        return JsonResponse(datos)

    def delete(self,request, id):
        invoice = list(Invoice.objects.filter(id=id).values())
        if len(invoice) > 0:
            Invoice.objects.filter(id=id).delete()
            datos = {'message': 'success'}
        else :
            datos = {'message': 'Invoice not found...'}
        return JsonResponse(datos)