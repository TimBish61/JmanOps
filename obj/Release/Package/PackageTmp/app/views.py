"""
Definition of views.
"""
import json

#used to generate GUID
#from uuid import uuid4
#import types

import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table,SimpleDocTemplate, Paragraph, Spacer

from reportlab.lib.units import cm,inch

from django.core.files.storage import FileSystemStorage

from reportlab.lib.styles import getSampleStyleSheet
from app.SalesOrderPdf import draw_pdf

#from app.OrderPdf import draw_header_test, draw_test, draw_pdf
from app.OrderPaginated import main, main_simple
from app.SalesOrderFlowPdf import main_simple, main, main_header

from app.XeroIntegration import MakeTestInvoice,MakeXeroInvoiceFromOrder,RefreshCustomerReceipts,RefreshXeroAll,MakeXeroContact

from django.contrib.sites import requests

from django.core import serializers


from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

import requests

from django.http import HttpRequest, HttpResponse, request
from django.template import RequestContext
from datetime import datetime




from django.http import HttpResponseRedirect
from app.models import Customer,Contact,SoHeader,SoDetail2,SYSTEM_SEQCONTRL,Currency,ExchangeRates,XeroTranView
from app.forms import CustomerForm,ContactForm,ContactFormNew,SoDetailFormSetNew,SoDetailFormSetEdit,SoHeaderForm

from django.http import JsonResponse
import json
from django.core import serializers
from django.http import QueryDict

#from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView,TemplateView,FormView

from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string

from django import forms

import datetime

def add_Test_invoice(request):
    MakeTestInvoice()

    tmpl_vars = {
    }
    return render(request, 'app/index.html', tmpl_vars)

def add_Xero_invoice(request, pk):
    new_invoice=MakeXeroInvoiceFromOrder(pk)

    #return from new_invoice
    # ['InvoiceID']	'3c3dbd0c-05ce-4ccd-abb1-79b0c544c26b'	str
	#['InvoiceNumber']	'INV-0005'	str
	#['HasErrors']	False	bool
	#['Status']	'DRAFT'	str
	#['Warnings']	[]	list

    returndata = {"title": "Xero Save Confirmation",
                  "message": "Success",
                  "ID": new_invoice[0]['InvoiceID']
                 ,"InvNo": new_invoice[0]['InvoiceNumber']
    }
    return render(request, 'app/Xero/APIReturn.html', returndata)

def get_Xero_Receipts(request):
    payments=RefreshXeroAll()

    #return from new_invoice
    # ['InvoiceID']	'3c3dbd0c-05ce-4ccd-abb1-79b0c544c26b'	str
	#['InvoiceNumber']	'INV-0005'	str
	#['HasErrors']	False	bool
	#['Status']	'DRAFT'	str
	#['Warnings']	[]	list

    #returndata = {"title": "Xero Save Confirmation",
    #              "message": "Success",
    #              "ID": new_invoice[0]['InvoiceID']
    #             ,"InvNo": new_invoice[0]['InvoiceNumber']
    #}

    returndata={"title": "Save Confirmation",
               "message": "All Objects successfully updated from Xero",}
    return render(request, 'app/Xero/APIReturn.html', returndata)


def add_new_contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        #form.EnteredBy=request.user
        #form.save(commit=True)
        #list_data = json.loads(request.POST['json_data'])
        response_data={}
        cst_id = int(request.POST.get('cst_id'))
        cst_Code = request.POST.get('cst_Code')

        #form.is_valid()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.EnteredBy = request.user
            instance.RecordCode = cst_Code
            instance.RecordType = 'Customer'
            instance.save()
            #form.save(commit=True)
            #return JsonResponse({'msg': 'Data saved'})
            response_data['result'] = 'Create post successful!'
            response_data['postpk'] = cst_id
            response_data['postCode'] = cst_Code
            return JsonResponse({'oPost': response_data})
        else:
            messages.error(request, "Error")
            #print("ERROR FORM INVALID")
            return JsonResponse({'msg': 'ERROR FORM INVALID'})
    else:
        form = ContactForm()

    #return JsonResponse({'form': form})
    return JsonResponse({'nothing to see': "this isn't happening"})

def contact_edit(request):
    #if request.method == "GET":
    #    id=request.GET.get('id')
    #    data = {'id': 0}
    #    #form = ItemForm(initial=data)
    #    form = ContactForm(initial=data)

    if request.method == "POST":
        
        id=request.POST.get('id')

        if id is None or id=='' : 
            data = {'id': 0}
            form = ContactForm(request.POST, data)
            cst_Code = 'TB01'
            cst_Type = 'Customer'
        else:
            #get the hidden data from existing database values because not in the form
            #oContact=Contact.objects.filter(id=id)[0:1]
            oContact=get_object_or_404(Contact, pk=id)
            cst_id = oContact.id
            cst_Code = oContact.RecordCode
            cst_Type = oContact.RecordType

            form = ContactForm(request.POST,instance=oContact)

        response_data={}
        #cst_Code = request.POST.get('RecordCode')
        #cst_Code = request.POST.get('cst_Code')

        #form.is_valid()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.EnteredBy = request.user
            instance.RecordCode = cst_Code
            instance.RecordType = cst_Type
            instance.save()
            #form.save(commit=True)
            #return JsonResponse({'msg': 'Data saved'})
            response_data['result'] = 'Create post successful!'
            response_data['postpk'] = id
            response_data['postCstCode'] = cst_Code
            return JsonResponse({'oPost': response_data})
        else:
            messages.error(request, "Error")
            #print("ERROR FORM INVALID")
            return JsonResponse({'msg': 'ERROR FORM INVALID'})
    else:
        form = ContactForm()

    #return JsonResponse({'form': form})
    return JsonResponse({'nothing to see': "this isn't happening"})

def delete_contact(request):
    if (request.method == 'POST'):
        id=request.POST.get('id');
        oContact=get_object_or_404(Contact, pk=id)
        cst_Code = oContact.RecordCode

        oContact.delete();

        response_data={}

        response_data['result'] = 'Delete post successful!'
        response_data['postpk'] = id
        response_data['postCode'] = cst_Code


        return JsonResponse({'oPost': response_data})
    else:
        return JsonResponse({'nothing to see': "this isn't happening"})

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactFormNew
    template_name = 'app/contact/contact_create_form.html'

    def form_valid(self, form):
        cst_Code = self.request.POST.get('RecordCode')
        cst_Type = self.request.POST.get('RecordType')
        instance = form.save(commit=False)
        instance.EnteredBy = self.request.user
        instance.RecordCode=cst_Code
        instance.RecordType=cst_Type
        instance.save()
        response_data={}
        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = instance.id
        response_data['Name'] = instance.Name
        response_data['postCstCode'] = cst_Code
        return JsonResponse({'oPost': response_data})
    def form_invalid(self, form):

        cst_Code = self.request.POST.get('RecordCode')
        response_data={}
        response_data['result'] = 'Save Error!' + form.errors['Email'][0]
        response_data['postpk'] = 99
        response_data['Name'] = 'Error'
        response_data['postCstCode'] = 'TTT'
        return JsonResponse({'oPost': response_data})

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'app/contact/contact_edit_form.html'

    def dispatch(self, *args, **kwargs):
        self.item_id = kwargs['pk']
        return super(ContactUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        objContact = Contact.objects.get(id=self.item_id)
        return HttpResponse(render_to_string('app/contact/contact_edit_form_success.html', {'contact': objContact}))

def UpdateCurrencyTable(request):

    response = requests.get('https://free.currencyconverterapi.com/api/v5/currencies')
    oData = response.json()
    oData=oData['results']

    for k,v in oData.items():
        try:
            cSymbol=v['currencySymbol']
        except:
            cSymbol=''

        new_entry = Currency(Code=v['id'], Name=v['currencyName'], Symbol=cSymbol)
        new_entry.save()

    tmpl_vars = {
    }
    return render(req, 'app/index.html', tmpl_vars)
   
def ContactList(request):
    template_name='app/contact/contact_list.html'

    if request.method=='POST':
        code=request.POST['code']
    else:
        code=''


    oContacts=Contact.objects.filter(RecordCode__exact=code).order_by('id')


    if 'lang' in request.COOKIES:
        language=request.COOKIES['lang']

    if 'lang' in request.session:
        session_language=request.session['lang']

    language='en-gb'
    session_language='en-gb'

    

    args={}
    #args.update(csrf(request))
    args['oContacts']=oContacts
    args['language']=language
    args['session_language']=session_language


    return render(request,template_name,args)   

def CurrencyList(request):
    response = requests.get('https://free.currencyconverterapi.com/api/v5/currencies')
    oData = response.json()
    oData=oData['results']
    #newd = {}
    #for key, value in oData.items():
    #    newd(key,value)
    
    #    mydicts = {k: dict(v) for k, v in oData.items()}

    #dic2=mydicts['mydict']['A']

    #{"results":{"ALL":{"currencyName":"Albanian Lek","currencySymbol":"Lek","id":"ALL"},"XCD":{"currencyName":"East Caribbean Dollar","currencySymbol":"$","id":"XCD"},"EUR":{"currencyName":"Euro","currencySymbol":"€","id":"EUR"}}}
    #oData = {'currencyName': 'Euro', 'currencySymbol': '€', 'id': 'EUR'}
    #"EUR":{"currencyName":"Euro","currencySymbol":"€","id":"EUR"}
    #args: {'currencyName': CurrencyData['EUR'],
    #    'currencySymbol': CurrencyData['country_name']


    #    }

    return render(request, 'app/Currency/currency_list.html', {'oData': oData})

def home(req):

    tmpl_vars = {
    }
    return render(req, 'app/index.html', tmpl_vars)
  
#this is the live save function inc Xero
def create_custpost(request):
    if request.method == 'POST':
        post_Code = request.POST.get('Code')
        post_Name = request.POST.get('Name')
        post_Address = request.POST.get('Address')
        post_PostCode = request.POST.get('PostCode')
        post_currency_code = request.POST.get('currency_code')
        post_id = int(request.POST.get('id'))

        response_data={}

        #request_data = {'Code': post_Code, 'Name': post_Name, 'Address': post_Address, 'PostCode': post_PostCode}
        
        if post_id==0:
            post = Customer(Code=post_Code, Name=post_Name, Address=post_Address, PostCode=post_PostCode, currency_code=post_currency_code)
        else:
            post = Customer.objects.get(id=post_id)
            post.Name=post_Name
            post.Address=post_Address
            post.PostCode=post_PostCode
            post.currency_code=post_currency_code
               
        post.save()



        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.id
        response_data['postCode'] = post.Code
        #response_data['text'] = post.text
        #response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        #response_data['author'] = post.author.username

        #finally update Xero
        MakeXeroContact(post.id)
        response_data['result'] = 'Record saved and update to Xero!'

        return JsonResponse({'oPost': response_data})

        #return HttpResponse(
        #    json.dumps(response_data),
        #    content_type="application/json"
        #)
    else:
        #return HttpResponse(
        #    json.dumps({"nothing to see": "this isn't happening"}),
        #    content_type="application/json"
        #)
        return JsonResponse({'nothing to see': "this isn't happening"})   
           
class CustomerView(UpdateView):
    template_name='app/Customer/customer.html'
   
    def get(self,request):

        data = {'id': 0, 'currency_code': 153}
        form = CustomerForm(initial=data)
        
        args={'form': form, 'title': 'Customers','posts': data}
        return render(
                request,
                self.template_name,args
                )

    def post(self,request):
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')

        args={'form': form,'title':text,'posts': posts}
        return render(request,self.template_name,args)
    
class CustomerMoveView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'app/Customer/customerfields.html'

    def dispatch(self, *args, **kwargs):
        #self.request.item_id = kwargs['pk']
        return super(CustomerMoveView, self).dispatch(*args, **kwargs)

    #def get(self,request):

    #    data = {'id': 0, 'Code': 'Empty'}
    #    form = CustomerForm(initial=data)
        
    #    args={'form': form, 'title': 'Customers','posts': data}
    #    return render(
    #            request,
    #            self.template_name,args
    #            )
    
    def post(self,request):
        myid = self.request.POST.get('postpk')
        mvtype=self.request.POST.get('postdir')
        form=self.request.POST.get('form')

        #oCustomer1 = get_object_or_404(Customer, id=myid)
        oCustomer1 = Customer.objects.filter(id=myid).order_by('id')[0:1]


        if not oCustomer1.exists():
            if mvtype=='prev':
                myid = Customer.objects.latest('id').id
                oCustomer_move = Customer.objects.filter(id=myid).order_by('id')[0:1]
            elif mvtype=='next':
                myid=0
                oCustomer_move = Customer.objects.filter(id__gt=myid).order_by('id')[0:1] 
            elif mvtype=='equals':
                myid=0
                oCustomer_move = oCustomer1 
        elif mvtype=='next':
            oCustomer_move = Customer.objects.filter(id__gt=oCustomer1[0].id).order_by('id')[0:1]
        elif mvtype=='prev':
            oCustomer_move = Customer.objects.filter(id__lt=oCustomer1[0].id).order_by('-id')[0:1]
        elif mvtype=='equals':
            oCustomer_move = oCustomer1


        if oCustomer_move.exists():
            #data = {'id': oCustomer_move[0].id, 'Code': oCustomer_move[0].Code, 'Name': oCustomer_move[0].Name, 'Address': oCustomer_move[0].Address, 'PostCode': oCustomer_move[0].PostCode}
            data = {'id': oCustomer_move[0].id}
        else:
            data = {'id': 0}


        
        form = CustomerForm(form, instance=oCustomer_move[0])
        #oCustomerMoveTo = get_object_or_404(Customer, id=myid)
        
        args={'form': form,'title':'Customer','oPost': data}
        #args={'title':'Customer','oPost': oCustomerMoveTo}

        return render(request, self.template_name, args)

def customer_move(request):
    if request.method == 'POST':
        myid = request.POST.get('postpk')
        mvtype=request.POST.get('postdir')

        #oCustomer1 = get_object_or_404(Customer, id=myid)
        oCustomer1 = Customer.objects.filter(id=myid).order_by('id')[0:1]


        if not oCustomer1.exists():
            if mvtype=='prev':
                myid = Customer.objects.latest('id').id
                oCustomer_move = Customer.objects.filter(id=myid).order_by('id')[0:1]
            elif mvtype=='next':
                myid=0
                oCustomer_move = Customer.objects.filter(id__gt=myid).order_by('id')[0:1] 
            elif mvtype=='equals':
                myid=0
                oCustomer_move = oCustomer1 
        elif mvtype=='next':
            oCustomer_move = Customer.objects.filter(id__gt=oCustomer1[0].id).order_by('id')[0:1]
        elif mvtype=='prev':
            oCustomer_move = Customer.objects.filter(id__lt=oCustomer1[0].id).order_by('-id')[0:1]
        elif mvtype=='equals':
            oCustomer_move = oCustomer1


        if oCustomer_move.exists():
            #data = {'id': oCustomer_move[0].id, 'Code': oCustomer_move[0].Code, 'Name': oCustomer_move[0].Name, 'Address': oCustomer_move[0].Address, 'PostCode': oCustomer_move[0].PostCode}
            data = {'id': oCustomer_move[0].id, 'Code': oCustomer_move[0].Code, 'Name': oCustomer_move[0].Name, 'Address': oCustomer_move[0].Address}
        else:
            data = {'id': 0, 'Code': '', 'Name': ''}

        #oReturnCustomer = serializers.serialize('json', oCustomer_move)
        #oReturnCustomer=oCustomer_move.values()
        oReturnCustomer=serializers.serialize('json', list(oCustomer_move))
        #oReturnCustomer= list(oCustomer_move.values())
        
        #return JsonResponse({'oReturnCustomer': oReturnCustomer }, safe=False)

        return JsonResponse({'oPost': data, 'oReturnCustomer': oReturnCustomer})

        #return JsonResponse({'oPost': data })

        #return HttpResponse(
        #    json.dumps(response_data),
        #    content_type="application/json"
        #)
    else:
        #return HttpResponse(
        #    json.dumps({"nothing to see": "this isn't happening"}),
        #    content_type="application/json"
        #)
        return JsonResponse({'nothing to see': "this isn't happening"})

def customer_trans(request):
    if request.method == 'POST':
        myid = request.POST.get('postpk')

        #oCustomer1 = get_object_or_404(Customer, id=myid)
        #oTrans = SoDetail2.objects.filter(account=myid).order_by('SOLineNumber')
        oTrans = XeroTranView.objects.filter(ContactNumber__exact=myid).order_by('Date','UpdatedDateUTC')

    if 'lang' in request.COOKIES:
            language=request.COOKIES['lang']

    if 'lang' in request.session:
        session_language=request.session['lang']

    language='en-gb'
    session_language='en-gb'

    

    args={}
    #args.update(csrf(request))
    #if oTrans:
    args['oTrans']=oTrans
    args['language']=language
    args['session_language']=session_language


    return render(request,'app/Customer/CustTrans.html',args)

def delete_customer(request):
    if (request.method == 'POST'):
        post_id=request.POST.get('id');
        post_Code=request.POST.get('Code');

        post = Customer.objects.get(id=post_id)
        post.delete();

        response_data={}

        response_data['result'] = 'Delete post successful!'
        response_data['postpk'] = post_id
        response_data['postCode'] = post_Code

        return JsonResponse({'oPost': response_data})
    else:
        return JsonResponse({'nothing to see': "this isn't happening"})

def customer_search(request):

    if request.method=='POST':
        search_text=request.POST['search_text']
    else:
        search_text=''

    foundCustomers=Customer.objects.filter(Name__contains=search_text)

    if 'lang' in request.COOKIES:
        language=request.COOKIES['lang']

    if 'lang' in request.session:
        session_language=request.session['lang']

    language='en-gb'
    session_language='en-gb'

    

    args={}
    #args.update(csrf(request))
    args['foundCustomers']=foundCustomers
    args['language']=language
    args['session_language']=session_language


    return render(request,'app/customer/CustSearch.html',args)

def customer_lookup(request):

    if request.method=='POST':
        search_text=request.POST['search_text']
    else:
        search_text=''

    foundCustomers=Customer.objects.filter(Name__contains=search_text)

    if 'lang' in request.COOKIES:
        language=request.COOKIES['lang']

    if 'lang' in request.session:
        session_language=request.session['lang']

    language='en-gb'
    session_language='en-gb'

    

    args={}
    #args.update(csrf(request))
    args['foundCustomers']=foundCustomers
    args['language']=language
    args['session_language']=session_language


    return render(request,'order/CustSearch.html',args)

def OrderList(request):
    template_name='app/SOrders/order_list.html'

    if request.method=='POST':
        code=request.POST['code']
    else:
        code=''

    #oContacts=SoHeader.objects.filter(RecordCode__exact=code).order_by('id')
    oOrders=SoHeader.objects.order_by('id')

    if 'lang' in request.COOKIES:
        language=request.COOKIES['lang']

    if 'lang' in request.session:
        session_language=request.session['lang']

    language='en-gb'
    session_language='en-gb'

    args={}

    args['oOrders']=oOrders
    args['language']=language
    args['session_language']=session_language


    return render(request,template_name,args)   

def SOrderDelete(request,pk):
    myid=pk

    #Post.objects.filter(pub_date__gt=datetime.now()).delete()
    SoDetail2.objects.filter(soheader__exact=myid).delete()
    #postdetail = SoDetail2.objects.get(soheader__exact=myid)
    #postdetail.delete();

    post = SoHeader.objects.get(id=myid)
    post.delete();

    response_data={}

    response_data['result'] = 'Delete post successful!'
    response_data['postpk'] = myid

    
    template_name='app/SOrders/order_list.html'
    model = SoHeader
    #success_url = reverse_lazy('order-list')
    return render(request,template_name,response_data)
    

class order2(CreateView):
    CreateView.template_name='app/SOrders/order_ajax.html'
    model = SoHeader
    form_class = SoHeaderForm
    #fields = ['customer','order_date','required_date','SONumber','SOReference','SOCurrency','SOExRate']
    #labels={'customer': 'customer','order_date': 'Date','required_date': 'Required','SONumber': 'Number','SOReference': 'Reference','SOCurrency': 'Currency','SOExRate': 'Rate'}
    success_url = reverse_lazy('order-list')

    def get_form(self, form_class=None):
        form = super(order2, self).get_form(self.get_form_class())
        form.fields['order_date'].widget.attrs.update({'class': 'datepicker'})
        form.fields['required_date'].widget.attrs.update({'class': 'datepicker'})
        #form.fields['SODescription'].widget.attrs.update({'size': '800'})

        #SOCurrency
        #form.fields['SOCurrency'] = forms.ModelChoiceField(queryset=Currency.objects.order_by('Code'))

        #set initial form values
        form.initial['SOCurrency']=153 #GBP


        return form

    def increment_invoice_number(self):
        oSequence = SYSTEM_SEQCONTRL.objects.filter(CTL_TABLE__exact='SoHeader').filter(CTL_FIELD__exact='SONumber')
        first_modified_date=datetime.date.today()
        if not oSequence:
            #create the sequence record
            new_entry = SYSTEM_SEQCONTRL(CTL_TABLE='SoHeader', CTL_FIELD='SONumber', CTL_SEQ_NUMBER=1, CTL_SEQ_LAST_INTEGRATION_DATEIME=first_modified_date)
            new_entry.save() # this will insert
            seq_number = 0
        else:
            seq_number = oSequence[0].CTL_SEQ_NUMBER
            seq_id=oSequence[0].id

            #update the sequence table
            t = SYSTEM_SEQCONTRL.objects.get(id=seq_id)
            t.CTL_SEQ_NUMBER = seq_number+1  # change field
            t.save() # this will update only

        return seq_number

    def get_initial(self):
        nextno=self.increment_invoice_number()
        return {'SONumber': nextno }

    def get_context_data(self, **kwargs):
        data = super(order2, self).get_context_data(**kwargs)
        #data['NextOrderNo'] = 11
        if self.request.POST:
            data['fSetOrderdetails'] = SoDetailFormSetNew(self.request.POST)
        else:
            data['fSetOrderdetails'] = SoDetailFormSetNew()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        
        fSetOrderdetails = context['fSetOrderdetails']

        with transaction.atomic():

            if fSetOrderdetails.is_valid() and fSetOrderdetails.has_changed():

                #'set fields in the main form'
                
                self.object = form.save(commit=False)
                mainForm=self.object
                mainForm.account=mainForm.customer.Code
                mainForm.SOCurrencycode=mainForm.SOCurrency.Code
                mainForm.user= self.request.user
                mainForm.save()


                fSetOrderdetails.instance = self.object

                #'set fields in the formset forms'
                new_instances = fSetOrderdetails.save(commit=False)

                for new_instance in new_instances:
                    new_instance.account = mainForm.customer.Code 
                    new_instance.SONumber = mainForm.SONumber
                    new_instance.itemcode=new_instance.item.Code
                    new_instance.analysiscode=new_instance.analysis.Code
                    new_instance.vatcode=new_instance.vat.Code
                    new_instance.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))

        return super(order2, self).form_valid(form)

class SOrderUpdate(UpdateView):
    template_name='app/Sorders/order_ajax.html'
    model = SoHeader
    form_class = SoHeaderForm

    success_url = reverse_lazy('order-list')


    def get_form(self, form_class=None):
        form = super(SOrderUpdate, self).get_form(self.get_form_class())
        form.fields['order_date'].widget.attrs.update({'class': 'datepicker'})
        form.fields['required_date'].widget.attrs.update({'class': 'datepicker'})

        return form

    def get_context_data(self, **kwargs):
        data = super(SOrderUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['fSetOrderdetails'] = SoDetailFormSetEdit(self.request.POST, instance=self.object)
        else:
            data['fSetOrderdetails'] = SoDetailFormSetEdit(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        fSetOrderdetails = context['fSetOrderdetails']
        #with transaction.atomic():
        #    self.object = form.save()

        #    if fSetOrderdetails.is_valid():
        #        fSetOrderdetails.instance = self.object
        #        fSetOrderdetails.save()
        with transaction.atomic():

            #if form.is_valid() and form.has_changed():
            if fSetOrderdetails.is_valid():

                #'set fields in the main form'
                
                self.object = form.save(commit=False)
                mainForm=self.object
                mainForm.account=mainForm.customer.Code
                mainForm.SOCurrencycode=mainForm.SOCurrency.Code
                mainForm.user= self.request.user
                mainForm.save()

                fSetOrderdetails.instance = self.object

                #'set fields in the formset forms'
                new_instances = fSetOrderdetails.save(commit=False)

                #lineno=int(fSetOrderdetails.management_form.data['tosoheader-TOTAL_FORMS'])
                lineno=int(fSetOrderdetails.management_form.data['tosoheader-INITIAL_FORMS'])+1

                for new_instance in new_instances:
                    new_instance.account = mainForm.customer.Code 
                    new_instance.SONumber = mainForm.SONumber
                    new_instance.itemcode=new_instance.item.Code
                    new_instance.analysiscode=new_instance.analysis.Code
                    new_instance.vatcode=new_instance.vat.Code

                    if new_instance.SOLineNumber==0:
                        new_instance.SOLineNumber=lineno

                    new_instance.save()

                    lineno += 1


                for delform in fSetOrderdetails.deleted_objects:
                    delform.delete()
            else:
                return self.render_to_response(self.get_context_data(form=form))
        
        return super(SOrderUpdate, self).form_valid(form)

def setCurrency(request):
    if request.method == 'POST':
        myid = request.POST.get('postpk')        

        #oCustomer1 = get_object_or_404(Customer, id=myid)
        oCustomer1 = Customer.objects.filter(id=myid).order_by('id')[0:1]

        myCurrId=oCustomer1[0].currency_code

        if oCustomer1.exists():
            if myCurrId!='':
                oCurrency = Currency.objects.filter(id=myCurrId).order_by('Code')[0:1]
                CurrencyCode=oCurrency[0].Code
            else:
                CurrencyCode=''
            
            data = {'id': oCustomer1[0].id, 'Code': oCustomer1[0].Code, 'Name': oCustomer1[0].Name, 'Address': oCustomer1[0].Address, 'PostCode': oCustomer1[0].PostCode, 'CurrencyId': myCurrId, 'CurrencyCode': CurrencyCode}

        else:
            data = {'id': 0, 'Code': '', 'CurrencyId': '', 'CurrencyCode':''}

        return JsonResponse({'oPost': data})
    else:
        return JsonResponse({'nothing to see': "this isn't happening"})

def setCurrencyRate(request):
    
    if request.method=='POST':
        currency=request.POST['currency_code']
    else:
        currency=''

    def get_rate():
        #check if we have a stored rate for today
        oRate = ExchangeRates.objects.filter(Code__exact=currency).filter(RateDate__exact=datetime.date.today())
        if not oRate:
            #create the exchange record if not stored
            sURL='https://free.currencyconverterapi.com/api/v5/convert?q=GBP_'+currency+'&compact=ultra'
            response = requests.get(sURL)
            oData = response.json()

            sKey='GBP_' +currency

            for k,v in oData.items():
                try:
                    if k==sKey:
                        rate=float(v)
                    else:
                        rate=float(9999)
                except:
                    rate=float(9999)

            new_entry = ExchangeRates(Code=currency,Name='',ExRate=rate, RateDate=datetime.date.today(), user=request.user)
            new_entry.save() # this will insert
            return rate
        else:
            #get the stored reco            
            rate=oRate[0].ExRate
            return rate

    if currency=='GBP':
        data = {'id': 0, 'Code': '','ExRate': 1}
        return JsonResponse({'oPost': data })
    else:
        rate=get_rate()
        data = {'id': 0, 'Code': '','ExRate': rate}

        return JsonResponse({'oPost': data })

def writePageNumberedDoc(request,pk):
    order = get_object_or_404(SoHeader, pk=pk)
    doc=main_simple("somefilename.pdf", order)
    fs = FileSystemStorage()

    with fs.open("somefilename.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        return response

    return response

#this is the main document sales order print
def write_pdf_view_doc(request, pk):

    order = get_object_or_404(SoHeader, pk=pk)
    doc=main_header("somefilename.pdf", order)

    #
    fs = FileSystemStorage()
    with fs.open("somefilename.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        response['Content-Disposition'] = 'filename="somefilename.pdf"'

    return response

def pdf_response(draw_funk, file_name, *args, **kwargs):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=\"%s\"" % file_name
    draw_funk(response, *args, **kwargs)
    return response

def CreatePdfTestView(request, pk):
    order = get_object_or_404(SoHeader, pk=pk)
    return pdf_response(draw_pdf, "Order.pdf", order)

def CreatePdfTestView3(request, pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4 )

    width, height = A4
    #A$: 210 x 297 mm
    #draw_test(p)
    draw_header_test(p,21, 29.7)
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #p.drawString(10, 800, "Sales Order ID:" + str(pk))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def CreatePdfTestView2(request,pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate("form_letter.pdf",pagesize=A4,
                    rightMargin=72,leftMargin=72,
                    topMargin=72,bottomMargin=18)

    Story=[]
    ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
        You will receive %s issues at the excellent introductory price of $%s. Please respond by\
        %s to start receiving your subscription and get the following free gift: %s.</font>'

    Story.append(Paragraph(ptext, styles["Justify"]))

    doc.build(Story)

