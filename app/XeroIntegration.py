from xero import Xero
from Crypto.PublicKey import RSA
from xero.auth import PrivateCredentials

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from app.models import Customer,Contact,SoHeader,SoDetail2,SYSTEM_SEQCONTRL,Currency,ExchangeRates, XeroPayments,XeroPaymentsInvoice,XeroSOInvLink,XeroOverPayments,XeroPrePayments
from app.models import XeroInvoices,XeroCreditNotes,XeroAllCreditNotes,XeroAllPayments,XeroAllInvoices,XeroAllOverPayments,XeroAllPrePayments,XeroAllPaymentAnalysis,XeroDatalinkTimer

import datetime as mydate
from datetime import datetime, timedelta

from django.conf import settings

from JmanOps.XeroSettings import XERO_CONSUMER_KEY, XERO_PRIVATE_KEY

#xero_config = {
#    "consumer_key": "PMIJ21PQIWMZKM5ASEE9T5URXLAI9W",
#    "consumer_secret": "1LHPUHJLHJKS52YMUUAXMYOKAPI9OQ",
#}

def XeroConnect():
#C:\Users\timbi\source\repos\JmanOps\JmanOps\app\static\app\xero
    with open(XERO_PRIVATE_KEY) as keyfile:     
        rsa_key = keyfile.read()
    credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key) 
    xero = Xero(credentials)
    return xero

def MakeTestInvoice():

    xero = XeroConnect()
    #datetime.date.today
    cr_date = datetime(2018, 5, 29, 18, 23, 29, 227)

    invoice = {"Type": "ACCREC",
              "Contact": {"Name": "John Doe"},
              "Date": cr_date,
              "DueDate": cr_date,
              "LineAmountTypes":"Exclusive",
                "LineItems":{ 
                            "LineItem": {
                                        "Description": 'Server Cost for Sept 2007'
                                        ,"Quantity": 20
                                        ,"UnitAmount": 500
                                        ,"AccountCode": "200" 
                            },
                }
    }

    new_invoice = xero.invoices.put(invoice)
        #return from new_invoice
         # ['InvoiceID']	'3c3dbd0c-05ce-4ccd-abb1-79b0c544c26b'	str
		#['InvoiceNumber']	'INV-0005'	str
		#['HasErrors']	False	bool
		#['Status']	'DRAFT'	str
		#['Warnings']	[]	list
    return

def MakeXeroInvoiceFromOrder(pk):

    xero = XeroConnect()

    #order = get_object_or_404(SoDetail2, pk=pk)
   # order=SoDetail2.objects.get(pk=pk)
   #soheader_id=6
    order=SoDetail2.objects.filter(soheader_id__exact=pk)
    contact=Contact.objects.filter(RecordCode__exact=order[0].soheader.customer.Code)


    #----Order fields------------
    #order.soheader.customer.Code
    #order[0].soheader.customer.Name
    #order.soheader.customer.Address
    #order.soheader.customer.Town
    #order.soheader.customer.County
    #order.soheader.customer.PostCode
    #order.soheader.customer.Country

    #order.SONumber

    #order.soheader.SOExRate
    #order.soheader.SOCurrency.Code
    #order.soheader.SOCurrency.Symbol

    #order.soheader.SODescription
    #order.soheader.SONumber
    #order.soheader.SOReference
    #order.soheader.order_date
    #order.soheader.required_date

    #order.SOLineNumber
    #order.SOQty
    #order.SOSalesPrice
    #order.SODetail
    #order.SONet
    #order.SOVat
    #order.SOHomeNet

    #order.item.Code
    #order.item.Name
    #order.itemcode

    #order.analysis.Code
    #order.analysis.Name
    #order.analysiscode

    #order.vat.Code
    #order.vat.Name
    #order.vat.VATRate
    #order.vatcode



    #datetime.date.today
    #cr_date = datetime(2018, 5, 29, 18, 23, 29, 227)
    inv_date=mydate.datetime.now()
    inv_duedate=mydate.datetime.now()+timedelta(days=30)

    invoices=[]
    invoice = {
        "Type": "ACCREC",
        "Contact": {"Name":order[0].soheader.customer.Name
                    ,"ContactNumber":order[0].soheader.customer.Code 
                    ,"Addresses": {
                                "Address": {
                                           "AddressType": "STREET",
                                            "AttentionTo": contact[0].Name,
                                            "AddressLine1": order[0].soheader.customer.Address,
                                            "AddressLine2": "",
                                            "AddressLine3": "",
                                            "AddressLine4": "" ,
                                            "City": order[0].soheader.customer.Town,
                                            "Region": order[0].soheader.customer.County,
                                            "PostalCode": order[0].soheader.customer.PostCode,
                                            "Country": order[0].soheader.customer.Country,
                                            },
                                "Address": {
                                           "AddressType": "POBOX",
                                            "AttentionTo":  contact[0].Name,
                                            "AddressLine1": order[0].soheader.customer.Address,
                                            "AddressLine2": "",
                                            "AddressLine3": "",
                                            "AddressLine4": "" ,
                                            "City": order[0].soheader.customer.Town,
                                            "Region": order[0].soheader.customer.County,
                                            "PostalCode": order[0].soheader.customer.PostCode,
                                            "Country": order[0].soheader.customer.Country,
                                            },
                                },
                    },
        "Date": inv_date,
        "DueDate": inv_duedate,
        "Reference": order[0].soheader.SOReference,
        "CurrencyCode": order[0].soheader.SOCurrency.Code,
        "LineAmountTypes":"Exclusive",
        }


    LineItems=[]

    for oLine in order:
        LineItem={}
        LineItem={
            'Description': oLine.SODetail,
            'Quantity': oLine.SOQty,
            'UnitAmount': oLine.SOSalesPrice,
            'TaxAmount': oLine.SOVat,
            'AccountCode': "200",
        }
        LineItems.append(LineItem)

    #add line items to invoice dictionary
    invoice['LineItems']=LineItems

    #finally add status to avoid approval
    invoice['Status']= 'AUTHORISED'

    #add each invoice to invoices dictionary
    invoices.append(invoice)

    #invoices[0]['Contact']['Addresses']['Address']['AddressLine1']

    #A PUT method will create new data in Xero, whereas a POST will either create new data or update existing data in Xero
    new_invoice = xero.invoices.put(invoices)

    #now update the link table
    oSequence = XeroSOInvLink.objects.filter(InvoiceID__exact=new_invoice[0]['InvoiceID'],SOID__exact=order[0].soheader.id)
    #order[0].soheader.SOReference
    newrow={'InvoiceID':new_invoice[0]['InvoiceID'],'InvoiceNumber':new_invoice[0]['InvoiceNumber'],'SOID':order[0].soheader.id,'SONumber':order[0].soheader.SONumber,'Code':order[0].soheader.customer.Code}
    if not oSequence:
        #create         
        new_entry = XeroSOInvLink(**newrow)
        new_entry.save()
    else:
        #edit
        t = XeroSOInvLink.objects.get(PaymentID__exact=Payment['PaymentID'])
        t.__dict__.update(newrow)
        t.save()


    return new_invoice

    return

def MakeXeroContact(pk):

    xero = XeroConnect()
     
    oContact=get_object_or_404(Customer, pk=pk)
    oCurrency=get_object_or_404(Currency,id=oContact.currency_code)

    contacts=[]

    contact={}

    #only add contactID if its a record originating in Ops
    conID=oContact.XeroContactID
    if conID!=None and conID!='':
       contact['ContactID'] = conID

    contact['ContactNumber'] = oContact.Code
    contact['Name'] = oContact.Name
    contact['EmailAddress'] = oContact.Email
    contact['TaxNumber'] = oContact.CoVatNo
    contact['DefaultCurrency'] =  oCurrency.Code


    Addresses=[]


    Address = {}

    Address['AddressType']= "POBOX"

    #.replace('\r\n','<br />\n'), styleN)
    #try to teel with  line returns to split address into fields
    myaddress=oContact.Address.split('\r\n')
    lastline=''

    if len(myaddress)>0:
        Address['AddressLine1']= myaddress[0]
    if len(myaddress)>1:
        Address['AddressLine2']= myaddress[1]
    if len(myaddress)>2:
        Address['AddressLine3']= myaddress[2]
    if len(myaddress)>3:
        for x in range (3,len(myaddress)):
            if x==3:
                lastline= myaddress[3]
            else:
                lastline= lastline+'\r\n'+myaddress[x]
        Address['AddressLine4']=lastline

    Address['City']= oContact.Town
    Address['Region']= oContact.County
    Address['PostalCode']= oContact.PostCode
    Address['Country']= oContact.Country


    Addresses.append(Address)


    contact['Addresses'] =  Addresses

    #"Phones": {
    #            "Phone": {
    #                        "PhoneType": "DEFAULT",
    #                        "PhoneNumber": oContact.Name,
    #                        "PhoneAreaCode": order[0].soheader.customer.Address,
    #                        "PhoneCountryCode": "",

    #                        },
    #            "Phone": {
    #                        "PhoneType": "MOBILE",
    #                        "PhoneNumber": contact[0].Name,
    #                        "PhoneAreaCode": order[0].soheader.customer.Address,
    #                        "PhoneCountryCode": "",
    #                        },
    #            },



    contact2={
        #"ContactID":oContact.XeroContactID,
        "ContactNumber":oContact.Code,
        "Name":oContact.Name,
        #"ContactStatus":order[0].soheader.customer.Name,
        "EmailAddress":oContact.Email,
        #"SkypeUserName":order[0].soheader.customer.Name,
        #"BankAccountDetails":order[0].soheader.customer.Name,
        "TaxNumber":oContact.CoVatNo,
        #"AccountsReceivableTaxType":order[0].soheader.customer.Name,
        #"AccountsPayableTaxType":order[0].soheader.customer.Name,
        #"FirstName":order[0].soheader.customer.Name,
        #"LastName":oContact.Name,
        "DefaultCurrency":oCurrency.Code,
        "Addresses": {
                    "Address": {
                                "AddressType": "POBOX",
                                #"AttentionTo":  contact[0].Name,
                                "AddressLine1": oContact.Address,
                                "AddressLine2": "",
                                "AddressLine3": "",
                                "AddressLine4": "" ,
                                "City": oContact.Town,
                                "Region": oContact.County,
                                "PostalCode": oContact.PostCode,
                                "Country": oContact.Country,
                                },
                    },

        #"Phones": {
        #            "Phone": {
        #                        "PhoneType": "DEFAULT",
        #                        "PhoneNumber": oContact.Name,
        #                        "PhoneAreaCode": order[0].soheader.customer.Address,
        #                        "PhoneCountryCode": "",

        #                        },
        #            "Phone": {
        #                        "PhoneType": "MOBILE",
        #                        "PhoneNumber": contact[0].Name,
        #                        "PhoneAreaCode": order[0].soheader.customer.Address,
        #                        "PhoneCountryCode": "",
        #                        },
        #            },
        #"ContactPersons": {
        #    "ContactPerson": {
        #                "FirstName": "DEFAULT",
        #                "LastName": contact[0].Name,
        #                "EmailAddress": order[0].soheader.customer.Address,
        #                "IncludeInEmails": "",

        #                },
        #    "ContactPerson": {
        #                "FirstName": "DEFAULT",
        #                "LastName": contact[0].Name,
        #                "EmailAddress": order[0].soheader.customer.Address,
        #                "IncludeInEmails": "",
        #                },
        #    },
        },

    #add each contact to contacts dictionary
    #contacts.append(contact)

    #A PUT method will create new data in Xero, whereas a POST will either create new data or update existing data in Xero
    #pyXero.. put creates new, save creates or edits - it seems this depends on wether you supply the ID in the contact list

    new_contact = xero.contacts.save(contact)


    newrow={'XeroContactID': new_contact[0]['ContactID'], 'XeroUpdateFail':'False'}
   
    #now update the Ops customer record
    t = oContact
    t.__dict__.update(newrow)
    t.save()

    return 

def RefreshXeroAll():
    xero = XeroConnect()
    RefreshContactsAll(xero)
    RefreshCustomerAllPayments(xero)
    RefreshCustomerAllOverpayments(xero)
    RefreshCustomerAllPrepayments(xero)
    RefreshCustomerAllInvoices(xero)
    RefreshCustomerAllCreditNotes(xero)
    return

def RefreshContactsAll(xero):

    lastrundate=getLastRunDate('Contacts')
    oContacts=xero.contacts.filter(since=lastrundate)

    Contact={}
    for oLine in oContacts:
        Contact=getLineDic_AllContact(oLine)
        #'XeroContactID': oLine.get('ContactID', None),
        #'Code': oLine.get('AccountNumber', None),
        #'Name': oLine.get('Name', None),

        #update database - payments table
        #oSequence=None
        oContact = Customer.objects.filter(XeroContactID__exact=Contact['XeroContactID'])
        if oContact:
            oCurrency=get_object_or_404(Currency,id=oContact[0].currency_code)

        if not oContact and Contact['Code']!= None :
            oContact = Customer.objects.filter(Code__exact=Contact['Code'])
        if not oContact and Contact['Name']!= None :
            oContact = Customer.objects.filter(Name__exact=Contact['Name'])

        
        #ensure we have a code and currency
        if Contact['currency_code']==None:
            #this is GBP
            Contact['currency_code']='153'
        elif not oCurrency:
            Contact['currency_code']='153'
        else:
            Contact['currency_code']=oCurrency.id

        #code
        if Contact['Code']==None:
            sNameList=Contact['Name'].upper().split()
            if len(sNameList)>1:
                sCode=sNameList[1]
            else:
                sCode=sNameList[0]

            iNumber=1
            while iNumber<10:
                sNumber=str('0'+str(iNumber))
                sCode=sCode[:3]+sNumber
                oExists=Customer.objects.filter(Code__exact=sCode)

                if not oExists: 
                    break
                else:
                    iNumber+=1
                    
            
            Contact['Code']=sCode

        
        if not oContact:            
            #create 
            new_entry = Customer(**Contact)
            new_entry.save()
        else:
            #edit
            t = oContact[0]
            t.__dict__.update(Contact)
            t.save()           

    return 

def RefreshCustomerReceipts(xero):

    lastrundate=getLastRunDate('Payments')
    oPayments=xero.payments.filter(since=lastrundate)

    lPayments=[]
    Account={}
    Invoice={}

    for oLine in oPayments:
        Payment=getLineDic_Payment(oLine)
        Invoice=getLineDic_PaymentInvoice(oLine)

        #update database - payments table
        oSequence = XeroPayments.objects.filter(PaymentID__exact=Payment['PaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroPayments(**Payment)
            new_entry.save()
        else:
            #edit
            t = XeroPayments.objects.get(PaymentID__exact=Payment['PaymentID'])
            t.__dict__.update(Payment)
            t.save()

        #update database - invoice payments table
        oSequence = XeroPaymentsInvoice.objects.filter(InvoiceID__exact=Invoice['InvoiceID']).filter(PaymentID__exact=Invoice['PaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroPaymentsInvoice(**Invoice)
            new_entry.save()
        else:
            #edit
            t = XeroPaymentsInvoice.objects.get(InvoiceID__exact=Invoice['InvoiceID'], PaymentID__exact=Payment['PaymentID'])
            t.__dict__.update(Invoice)
            t.save()
            

    return 

def RefreshCustomerAllPayments(xero):

    lastrundate=getLastRunDate('Payments')
    oPayments=xero.payments.filter(since=lastrundate)

    lPayments=[]
    Account={}
    Object={}

    for oLine in oPayments:
        Payment=getLineDic_AllPayment(oLine)
        Object=getLineDic_AllPaymentAnalysis(oLine)

        #update database - payments table
        oSequence = XeroAllPayments.objects.filter(PaymentID__exact=Payment['PaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroAllPayments(**Payment)
            new_entry.save()
        else:
            #edit
            t = XeroAllPayments.objects.get(PaymentID__exact=Payment['PaymentID'])
            t.__dict__.update(Payment)
            t.save()

        #update database - payments analysis table
        oSequence = XeroAllPaymentAnalysis.objects.filter(ObjectID__exact=Object['ObjectID']).filter(PaymentID__exact=Object['PaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroAllPaymentAnalysis(**Object)
            new_entry.save()
        else:
            #edit
            t = XeroAllPaymentAnalysis.objects.get(ObjectID__exact=Object['ObjectID'], PaymentID__exact=Object['PaymentID'])
            t.__dict__.update(Object)
            t.save()
    return 

def RefreshCustomerOverpayments(xero):

    lastrundate=getLastRunDate('Overpayments')
    oXeroEndPoint=xero.overpayments.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_OverPayment(oLine)

        #update database - payments table
        oSequence = XeroOverPayments.objects.filter(OverpaymentID__exact=lineDictionary['OverpaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroOverPayments(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroOverPayments.objects.get(OverpaymentID__exact=lineDictionary['OverpaymentID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerAllOverpayments(xero):

    lastrundate=getLastRunDate('Overpayments')
    oXeroEndPoint=xero.overpayments.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_AllOverPayment(oLine)

        #update database - payments table
        oSequence = XeroAllOverPayments.objects.filter(OverpaymentID__exact=lineDictionary['OverpaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroAllOverPayments(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroAllOverPayments.objects.get(OverpaymentID__exact=lineDictionary['OverpaymentID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerPrepayments(xero):

    lastrundate=getLastRunDate('Prepayments')
    oXeroEndPoint=xero.prepayments.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_PrePayment(oLine)

        #update database - payments table
        oSequence = XeroPrePayments.objects.filter(PrepaymentID__exact=lineDictionary['PrepaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroPrePayments(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroPrePayments.objects.get(PrepaymentID__exact=lineDictionary['PrepaymentID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerAllPrepayments(xero):

    lastrundate=getLastRunDate('Prepayments')
    oXeroEndPoint=xero.prepayments.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_AllPrePayment(oLine)

        #update database - payments table
        oSequence = XeroAllPrePayments.objects.filter(PrepaymentID__exact=lineDictionary['PrepaymentID'])
        if not oSequence:
            #create 
            new_entry = XeroAllPrePayments(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroAllPrePayments.objects.get(PrepaymentID__exact=lineDictionary['PrepaymentID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerInvoices(xero):

    lastrundate=getLastRunDate('Invoices')
    oXeroEndPoint=xero.invoices.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_Invoice(oLine)

        #update database - payments table
        oSequence = XeroInvoices.objects.filter(InvoiceID__exact=lineDictionary['InvoiceID'])
        if not oSequence:
            #create 
            new_entry = XeroInvoices(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroInvoices.objects.get(InvoiceID__exact=lineDictionary['InvoiceID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerAllInvoices(xero):

    lastrundate=getLastRunDate('Invoices')
    oXeroEndPoint=xero.invoices.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_AllInvoice(oLine)

        #update database - payments table
        oSequence = XeroAllInvoices.objects.filter(InvoiceID__exact=lineDictionary['InvoiceID'])
        if not oSequence:
            #create 
            new_entry = XeroAllInvoices(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroAllInvoices.objects.get(InvoiceID__exact=lineDictionary['InvoiceID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerCreditNotes(xero):

    lastrundate=getLastRunDate('CreditNotes')
    oXeroEndPoint=xero.creditnotes.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_Credits(oLine)

        #update database - payments table
        oSequence = XeroCreditNotes.objects.filter(CreditNoteID__exact=lineDictionary['CreditNoteID'])
        if not oSequence:
            #create 
            new_entry = XeroCreditNotes(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroCreditNotes.objects.get(CreditNoteID__exact=lineDictionary['CreditNoteID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def RefreshCustomerAllCreditNotes(xero):

    lastrundate=getLastRunDate('CreditNotes')
    oXeroEndPoint=xero.creditnotes.filter(since=lastrundate)

    for oLine in oXeroEndPoint:
        lineDictionary=getLineDic_AllCredits(oLine)

        #update database - payments table
        oSequence = XeroAllCreditNotes.objects.filter(CreditNoteID__exact=lineDictionary['CreditNoteID'])
        if not oSequence:
            #create 
            new_entry = XeroAllCreditNotes(**lineDictionary)
            new_entry.save()
        else:
            #edit
            t = XeroAllCreditNotes.objects.get(CreditNoteID__exact=lineDictionary['CreditNoteID'])
            t.__dict__.update(lineDictionary)
            t.save()

    return 

def getLastRunDate(type):
        oSequence = SYSTEM_SEQCONTRL.objects.filter(CTL_TABLE__exact='Xero').filter(CTL_FIELD__exact=type)

        #test switch
        #last_modified_date=mydate.datetime.now()
        last_modified_date=mydate.datetime.now()-timedelta(days=10)
        
        first_modified_date=mydate.datetime.now()-timedelta(days=30)

        if not oSequence:
            #create the sequence record
            new_entry = SYSTEM_SEQCONTRL(CTL_TABLE='Xero', CTL_FIELD=type, CTL_SEQ_NUMBER=1, CTL_SEQ_LAST_INTEGRATION_DATEIME=first_modified_date)
            new_entry.save() # this will insert
            rundate = first_modified_date
        else:
            rundate = oSequence[0].CTL_SEQ_LAST_INTEGRATION_DATEIME
            seq_id=oSequence[0].id

            #update the sequence table
            t = SYSTEM_SEQCONTRL.objects.get(id=seq_id)
            t.CTL_SEQ_LAST_INTEGRATION_DATEIME = last_modified_date  # change field
            t.save() # this will update only

        return rundate

def getLineDic_AllContact(oLine):

    Contact={
        'XeroContactID': oLine.get('ContactID', None),
        'Code': oLine.get('ContactNumber', None),
        'Name': oLine.get('Name', None),
        'Email': oLine.get('EmailAddress', None),
        #'Address': Address,
        #'Town': Town,
        #'County':County,
        #'PostCode': PostCode,
        #'Country': Country,
        'CoVatNo': oLine.get('TaxNumber', None),        
        'currency_code': oLine.get('DefaultCurrency', None),
    }

    for oAddress in oLine.get('Addresses',{}):
        if oAddress.get('AddressType', None)=='POBOX':
            Contact['Address']=oAddress.get('AddressLine1',None)
            if oAddress.get('AddressLine2',None)!=None and oAddress.get('AddressLine2',None)!='':
                Contact['Address']+="\n"+oAddress.get('AddressLine2',None)
            if oAddress.get('AddressLine3',None)!=None and oAddress.get('AddressLine3',None)!='':
                Contact['Address']+="\n"+oAddress.get('AddressLine3',None)
            if oAddress.get('AddressLine4',None)!=None and oAddress.get('AddressLine4',None)!='':
                Contact['Address']+="\n"+oAddress.get('AddressLine4',None)

            Contact['Town']=oAddress.get('City',None)
            Contact['County']=oAddress.get('Region',None)
            Contact['PostCode']=oAddress.get('PostalCode',None)
            Contact['Country']=oAddress.get('Country',None)

    return Contact

def getLineDic_Payment(oLine):    
    oLineDictionary={}
    oLineDictionary={
        'PaymentID': oLine['PaymentID'],
        'Date': oLine['Date'],
        'BankAmount': oLine['BankAmount'],
        'Amount': oLine['Amount'],
        'Reference': oLine['Reference'],
        'CurrencyRate': oLine['CurrencyRate'],
        'PaymentType': oLine['PaymentType'],
        'Status': oLine['Status'],
        'UpdatedDateUTC': oLine['UpdatedDateUTC'],
        'IsReconciled': oLine['IsReconciled'],
        'AnalysisCode': oLine['Account']['Code'],
        }
    return oLineDictionary

def getLineDic_PaymentInvoice(oLine):    
    oLineDictionary={}
    oLineDictionary={
        'ContactID': oLine['Invoice']['Contact']['ContactID'],
        'ContactName': oLine['Invoice']['Contact']['Name'],
        'CurrencyCode': oLine['Invoice']['CurrencyCode'],
        'Type': oLine['Invoice']['Type'],
        'InvoiceID': oLine['Invoice']['InvoiceID'],
        'InvoiceNumber':oLine['Invoice']['InvoiceNumber'],
        'PaymentID': oLine['PaymentID'],
        }
    return oLineDictionary

def getLineDic_PrePayment(oLine):
    Prepayment={}
    Prepayment={
        'ContactID': oLine['Contact']['ContactID'],
        'Name': oLine['Contact']['Name'],
        'Date': oLine['Date'],
        'Status': oLine['Status'],
        'LineAmountTypes': oLine['LineAmountTypes'],
        'SubTotal': oLine['SubTotal'],
        'TotalTax': oLine['TotalTax'],
        'Total': oLine['Total'],
        'UpdatedDateUTC': oLine['UpdatedDateUTC'],
        'CurrencyCode': oLine['CurrencyCode'],
        'Type': oLine['Type'],
        'Reference': oLine['Reference'],
        'RemainingCredit': oLine['RemainingCredit'],
        'HasAttachments': oLine['HasAttachments'],
        'PrepaymentID': oLine['PrepaymentID'],
    }
    return Prepayment

def getLineDic_OverPayment(oLine):
    Overpayment={}
    Overpayment={
        'ContactID': oLine['Contact']['ContactID'],
        'Name': oLine['Contact']['Name'],
        'Date': oLine['Date'],
        'Status': oLine['Status'],
        'LineAmountTypes': oLine['LineAmountTypes'],
        'SubTotal': oLine['SubTotal'],
        'TotalTax': oLine['TotalTax'],
        'Total': oLine['Total'],
        'UpdatedDateUTC': oLine['UpdatedDateUTC'],
        'CurrencyCode': oLine['CurrencyCode'],
        'Type': oLine['Type'],
        'RemainingCredit': oLine['RemainingCredit'],
        'HasAttachments': oLine['HasAttachments'],
        'OverpaymentID': oLine['OverpaymentID'],
    }
    return Overpayment

def getLineDic_Invoice(oLine):
    Invoice={}
    Invoice={
        'ContactID': oLine['Contact']['ContactID'],
        'Name': oLine['Contact']['Name'],
        'Date': oLine['Date'],
        'DueDate': oLine['DueDate'],
        'Status': oLine['Status'],
        'LineAmountTypes': oLine['LineAmountTypes'],
        'SubTotal': oLine['SubTotal'],
        'TotalTax': oLine['TotalTax'],
        'Total': oLine['Total'],
        'UpdatedDateUTC': oLine['UpdatedDateUTC'],
        'CurrencyCode': oLine['CurrencyCode'],
        'Type': oLine['Type'],
        'InvoiceID': oLine['InvoiceID'],
        'InvoiceNumber': oLine['InvoiceNumber'],
        'AmountDue': oLine['AmountDue'],
        'AmountPaid': oLine['AmountPaid'],
        'AmountCredited': oLine['AmountCredited'],
        'CurrencyRate': oLine['CurrencyRate'],
        'HasAttachments': oLine['HasAttachments'],
    }
    return Invoice

def getLineDic_Credits(oLine):
    CreditNote={}
    CreditNote={
        'ContactID': oLine['Contact']['ContactID'],
        'Name': oLine['Contact']['Name'],
        'Date': oLine['Date'],
        'Status': oLine['Status'],
        'LineAmountTypes': oLine['LineAmountTypes'],
        'SubTotal': oLine['SubTotal'],
        'TotalTax': oLine['TotalTax'],
        'Total': oLine['Total'],
        'UpdatedDateUTC': oLine['UpdatedDateUTC'],
        'CurrencyCode': oLine['CurrencyCode'],
        'CurrencyRate': oLine['CurrencyRate'],
        'Type': oLine['Type'],
        'Reference': oLine['Reference'],
        'RemainingCredit': oLine.get('RemainingCredit', 0),
        'HasAttachments': oLine['HasAttachments'],
        'CreditNoteID': oLine['CreditNoteID'],
        'CreditNoteNumber': oLine['CreditNoteNumber'],
    }
    return CreditNote

def getLineDic_AllInvoice(oLine):
    Invoice={}
    Invoice={
        'Type': oLine.get('Type', None),
        'ContactID':oLine.get('Contact',{}).get('ContactID', None),
        'ContactNumber':oLine.get('Contact',{}).get('ContactNumber', None),
        'Name':oLine.get('Contact',{}).get('Name', None),
        'Date': oLine.get('Date', None),
        'DueDate': oLine.get('DueDate', None),
        'Status': oLine.get('Status', None),
        'LineAmountTypes': oLine.get('LineAmountTypes', None),

        'SubTotal': oLine.get('SubTotal', None),
        'TotalTax': oLine.get('TotalTax', None),
        'Total': oLine.get('Total', None),
        'TotalDiscount': oLine.get('TotalDiscount', None),
        'UpdatedDateUTC': oLine.get('UpdatedDateUTC', None),
        'CurrencyCode': oLine.get('CurrencyCode', None),
        'CurrencyRate': oLine.get('CurrencyRate', None),
        'InvoiceID': oLine.get('InvoiceID', None),
        'InvoiceNumber': oLine.get('InvoiceNumber', None),

        'Reference': oLine.get('Reference', None),
        'BrandingThemeID': oLine.get('BrandingThemeID', None),
        'Url': oLine.get('Url', None),
        'SentToContact': oLine.get('SentToContact', False),
        'ExpectedPaymentDate': oLine.get('ExpectedPaymentDate', None),
        'PlannedPaymentDate': oLine.get('PlannedPaymentDate', None),
        'HasAttachments': oLine.get('HasAttachments', False),




        'AmountDue': oLine.get('AmountDue', None),
        'AmountPaid': oLine.get('AmountPaid', None),
        'CISDeduction': oLine.get('CISDeduction', None),
        'FullyPaidOnDate': oLine.get('FullyPaidOnDate', None),
        'AmountCredited': oLine.get('AmountCredited', None),


    }
    return Invoice

def getLineDic_AllCredits(oLine):
    CreditNote={}
    CreditNote={
        'Type': oLine.get('Type', None),
        'ContactID':oLine.get('Contact',{}).get('ContactID', None),
        'ContactNumber':oLine.get('Contact',{}).get('ContactNumber', None),
        'Name':oLine.get('Contact',{}).get('Name', None),
        'Date': oLine.get('Date', None),
        'Status': oLine.get('Status', None),
        'LineAmountTypes': oLine.get('LineAmountTypes', None),
        'SubTotal': oLine.get('SubTotal', None),
        'TotalTax': oLine.get('TotalTax', None),
        'CISDeduction': oLine.get('CISDeduction', None),
        'UpdatedDateUTC': oLine.get('UpdatedDateUTC', None),
        'CurrencyCode': oLine.get('CurrencyCode', None),
        'FullyPaidOnDate': oLine.get('FullyPaidOnDate', None),
        'CreditNoteID': oLine.get('CreditNoteID', None),
        'CreditNoteNumber': oLine.get('CreditNoteNumber', None),
        'Reference': oLine.get('Reference', None),
        'SentToContact': oLine.get('SentToContact', False),
        'RemainingCredit': oLine.get('RemainingCredit', None),
        'BrandingThemeID': oLine.get('BrandingThemeID', None),
        'HasAttachments': oLine.get('HasAttachments', False),


    }
    return CreditNote

def getLineDic_AllPayment(oLine):    
    oLineDictionary={}
    oLineDictionary={
        'PaymentID': oLine.get('PaymentID', None),
        'AccountID':oLine.get('Account',{}).get('AccountID', None),
        'Code':oLine.get('Account',{}).get('Code', None),
        'Date': oLine.get('Date', None),
        'CurrencyRate': oLine.get('CurrencyRate', None),
        'BankAmount': oLine.get('BankAmount', None),
        'Amount': oLine.get('Amount', None),
        'Reference': oLine.get('Reference', None),
        'IsReconciled': oLine.get('IsReconciled', None),
        'Status': oLine.get('Status', None),
        'PaymentType': oLine.get('PaymentType', None),
        'UpdatedDateUTC': oLine.get('UpdatedDateUTC', None),
        'Code':oLine.get('Account',{}).get('Code', None),
        }
    return oLineDictionary

def getLineDic_AllPrePayment(oLine):
    Prepayment={}
    Prepayment={
        'ContactID':oLine.get('Contact',{}).get('ContactID', None),
        'Name':oLine.get('Contact',{}).get('Name', None),
        'ContactNumber':oLine.get('Contact',{}).get('ContactNumber', None),
        'Date': oLine.get('Date', None),
        'Status': oLine.get('Status', None),
        'LineAmountTypes': oLine.get('LineAmountTypes', None),
        'SubTotal': oLine.get('SubTotal', None),
        'TotalTax': oLine.get('TotalTax', None),
        'Total': oLine.get('Total', None),
        'UpdatedDateUTC': oLine.get('UpdatedDateUTC', None),
        'CurrencyCode': oLine.get('CurrencyCode', None),
        'Type': oLine.get('Type', None),
        'RemainingCredit': oLine.get('RemainingCredit', None),
        'HasAttachments': oLine.get('HasAttachments', False),
        'PrepaymentID': oLine.get('PrepaymentID', None),
        'CurrencyRate': oLine.get('CurrencyRate', None),
        'Reference': oLine.get('Reference', None),
        'FullyPaidOnDate': oLine.get('FullyPaidOnDate', None),

    }
    return Prepayment

def getLineDic_AllOverPayment(oLine):
    Overpayment={}
    Overpayment={
        'ContactID':oLine.get('Contact',{}).get('ContactID', None),
        'Name':oLine.get('Contact',{}).get('Name', None),
        'ContactNumber':oLine.get('Contact',{}).get('ContactNumber', None),
        'Date': oLine.get('Date', None),
        'Status': oLine.get('Status', None),
        'LineAmountTypes': oLine.get('LineAmountTypes', None),
        'SubTotal': oLine.get('SubTotal', None),
        'TotalTax': oLine.get('TotalTax', None),
        'Total': oLine.get('Total', None),
        'UpdatedDateUTC': oLine.get('UpdatedDateUTC', None),
        'CurrencyCode': oLine.get('CurrencyCode', None),
        'Type': oLine.get('Type', None),
        'RemainingCredit': oLine.get('RemainingCredit', None),
        'HasAttachments': oLine.get('HasAttachments', False),
        'OverpaymentID': oLine.get('OverpaymentID', None),
        'CurrencyRate': oLine.get('CurrencyRate', None),

    }
    return Overpayment

def getLineDic_AllPaymentAnalysis(oLine):    
    oLineDictionary={}
    oLineDictionary={
        'ContactID': oLine.get('Invoice',{}).get('Contact',{}).get('ContactID', None),
        'ContactNumber': oLine.get('Invoice',{}).get('Contact',{}).get('ContactNumber', None),
        'Name': oLine.get('Invoice',{}).get('Contact',{}).get('Name', None),
        'CurrencyCode': oLine.get('Invoice',{}).get('CurrencyCode', None),
        'Type':  oLine.get('Invoice',{}).get('Type', None),
        'ObjectID': oLine.get('Invoice',{}).get('InvoiceID', None),
        'ObjectNumber': oLine.get('Invoice',{}).get('InvoiceNumber', None),
        'PaymentID': oLine.get('PaymentID', None),
        }
    return oLineDictionary


  




