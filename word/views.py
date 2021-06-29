from django.http import HttpResponse
from django.views.generic import View
import datetime
from docx import Document
from io import StringIO
from io import BytesIO
from docx.shared import Inches
from django.contrib import messages
from formss.models import Monthly,Balance
from word.utils import render_to_pdf #created in step 4
from django.shortcuts import render,redirect
from django.db.models import Max,Sum
import itertools  


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        last_month1 =Monthly.objects.values_list('month',flat=True)
        b=0
        for z in last_month1:
            last_month = z
            b=b+1

        serial_no_list1 = Monthly.objects.filter(month=last_month).values_list('serial_No',flat=True)
        serial_no_list = []
        i=1
        for x in serial_no_list1:
            serial_no_list.append(i)
            i= i+1
        created_date_list = Monthly.objects.filter(month=last_month).values_list('created_date',flat=True)
        income_list = Monthly.objects.filter(month=last_month).values_list('income',flat=True)
        expenditure_list = Monthly.objects.filter(month=last_month).values_list('expenditure',flat=True)
        amount_list = Monthly.objects.filter(month=last_month).values_list('amount',flat=True)

        total_income1 = Monthly.objects.filter(expenditure='',month=last_month).aggregate(Sum('amount'))
        total_income = total_income1.get('amount__sum')

        total_expenditure1= Monthly.objects.filter(income='',month=last_month).aggregate(Sum('amount'))
        total_expenditure = total_expenditure1.get('amount__sum')

        if total_income ==None:
            profit_loss= -(total_expenditure)
        elif total_expenditure ==None:
            profit_loss= total_income
        else:
            profit_loss = total_income - total_expenditure

        last_pk1 = Balance.objects.order_by('id').aggregate(Max('id'))
        last_pk = last_pk1.get('id__max')
        old_balance =Balance.objects.values_list('old_balance', flat=True).get(id=last_pk)

        new_balance = int(old_balance) + profit_loss
        

        secondary = Balance(old_balance=new_balance)
        secondary.save()

        # for a in last_month1[b-1]:
        #     second_last_month  = a
        # if b>2:
        #     second_last_month  = last_month1[b-2]
        #     if last_month != second_last_month:
        #         secondary = Balance(old_balance=new_balance,id=id)
        #         secondary.save()

        combined_list = zip(serial_no_list,created_date_list,income_list,expenditure_list,amount_list)
        data = {
            'today': datetime.date.today(), 
            'last_month':last_month,
            'combined_list':combined_list,
            'total_income':total_income,
            'total_expenditure':total_expenditure,
            'profit_loss':profit_loss,
            'old_balance':old_balance,
            'new_balance':new_balance,
            'last_month':last_month,
       
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
        messages.info(request,'Thanks, your monthly updated')
        return render(request,'index.html')
    else:
        return render(request,'index.html')



def your_view(request):
    document = Document("my_word_file.docx")
    for paragraph in document.paragraphs:
        if 'Contact name' in paragraph.text:
            paragraph.text = 'new text containing ocean'
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)

    return response