from django.http import HttpResponse
from django.views.generic import View
import datetime
from formss.models import Monthly,Balance
from word.utils import render_to_pdf #created in step 4
from django.shortcuts import render,redirect
from django.db.models import Max,Sum
import itertools  


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
  
        serial_no_list = Monthly.objects.values_list('serial_No',flat=True)
        created_date_list = Monthly.objects.values_list('created_date',flat=True)
        income_list = Monthly.objects.values_list('income',flat=True)
        expenditure_list = Monthly.objects.values_list('expenditure',flat=True)
        amount_list = Monthly.objects.values_list('amount',flat=True)

        total_income1 = Monthly.objects.filter(expenditure=0).aggregate(Sum('amount'))
        total_income = total_income1.get('amount__sum')

        total_expenditure1= Monthly.objects.filter(income=0).aggregate(Sum('amount'))
        total_expenditure = total_expenditure1.get('amount__sum')

        profit_loss = total_income - total_expenditure

        combined_list = zip(serial_no_list,created_date_list,income_list,expenditure_list,amount_list)
        data = {
             'today': datetime.date.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            'month':'May',
            'combined_list':combined_list,
            'total_income':total_income,
            'total_expenditure':total_expenditure,
            'profit_loss':profit_loss,
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

def index(request):
    if request.method == 'POST':
        month = request.POST['month']
        year = request.POST['year']
        income = request.POST['income']
        expenditure = request.POST['expenditure']
        amount = request.POST['amount']
        obj1 = Monthly.objects.order_by('id').aggregate(Max('serial_No'))
        obj = obj1.get('serial_No__max')
        if obj == 0:
            obj=1
        else:
            obj= obj+1
        primary=Monthly( serial_No=obj,income=income,expenditure=expenditure,amount=amount,month=month,year=year)
        primary.save()
        return render(request,'index.html')
    else:
        return render(request,'index.html')