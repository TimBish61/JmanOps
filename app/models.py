"""
Definition of models.
"""
from __future__ import unicode_literals
#from django.core.urlresolvers import reverse

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


import datetime
#from app.models import Currency
from django.forms.models import BaseInlineFormSet

# Create your models here.
class SYSTEM_SEQCONTRL(models.Model):
    CTL_TABLE = models.CharField(max_length=128,default='',blank=True)
    CTL_FIELD = models.CharField(max_length=128,default='',blank=True)
    CTL_SEQ_NUMBER = models.IntegerField(default=0,blank=False)
    CTL_SEQ_LAST_INTEGRATION_DATEIME = models.DateTimeField()


    class Meta:
        unique_together = ('CTL_TABLE', 'CTL_FIELD',)

    def __str__(self):
        return self.CTL_TABLE+','+self.CTL_FIELD+': '+str(self.CTL_SEQ_NUMBER)



class Currency(models.Model):
    Code = models.CharField(unique=True,max_length=3,default='',blank=False)
    Name = models.CharField(max_length=100,default='',blank=True)
    Symbol = models.CharField(max_length=4,default='',blank=True,null=True)
    Entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code+': '+self.Name

class ExchangeRates(models.Model):
    Code = models.CharField(max_length=3,default='',blank=False)
    Name = models.CharField(max_length=100,default='',blank=True)
    ExRate = models.FloatField(default=1,null=True)
    RateDate = models.DateField(auto_now_add=True)
    Entered = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('Code', 'RateDate',)

    def __str__(self):
        return self.Code+': '+str(self.ExRate)

class SYSTEM_MAIN(models.Model):
    CompanyName = models.CharField(max_length=128,default='',blank=True)
    Address = models.TextField(max_length=160,default='',null=True,blank=True)
    Town = models.CharField(max_length=20,default='',blank=True)
    County = models.CharField(max_length=20,default='',blank=True)    
    PostCode = models.CharField(max_length=12,null=True,default='',blank=True)
    Country = models.CharField(max_length=20,default='',blank=True)
    Phone = models.CharField(max_length=20,default='',blank=True)
    Mobile = models.CharField(max_length=20,default='',blank=True)
    Email = models.CharField(max_length=64,default='',blank=True)
    Website = models.CharField(max_length=64,default='',blank=True)
    Curency=models.ForeignKey(Currency,on_delete=models.DO_NOTHING)
    CoVatNo = models.CharField(max_length=15,default='',blank=True)
    CoRegNo = models.CharField(max_length=20,default='',blank=True)

    def __str__(self):
        return self.CompanyName


class SYSTEM_BANK(models.Model):
    BankType=models.CharField(max_length=20,default='',blank=True)    
    Curency=models.ForeignKey(Currency,on_delete=models.DO_NOTHING)
    AccountName=models.CharField(max_length=128,default='',blank=True)
    BankName=models.CharField(max_length=128,default='',blank=True)
    BankSortCode=models.CharField(max_length=10,default='',blank=True)
    BankAccountNo=models.CharField(max_length=15,default='',blank=True)
    BankRef=models.CharField(max_length=18,default='',blank=True)
    BankIBAN=models.CharField(max_length=100,default='',blank=True)
    Address = models.TextField(max_length=160,default='',null=True,blank=True)
    Town = models.CharField(max_length=20,default='',blank=True)
    County = models.CharField(max_length=20,default='',blank=True)    
    PostCode = models.CharField(max_length=12,null=True,default='',blank=True)
    Country = models.CharField(max_length=20,default='',blank=True)

    def __str__(self):
        return self.BankType+': '+self.BankName

class Customer(models.Model):
    Code = models.CharField(unique=True,max_length=10,default='',blank=False,db_index=True)
    currency_code=models.CharField(max_length=3,default='',blank=True)
    Name = models.CharField(max_length=100,default='',null=True,blank=True,db_index=True)
    Address = models.TextField(default='',null=True,blank=True)
    Town = models.CharField(max_length=20,default='',null=True,blank=True)
    County = models.CharField(max_length=20,default='',null=True,blank=True)    
    PostCode = models.CharField(max_length=12,null=True,default='',blank=True)
    Country = models.CharField(max_length=20,default='',null=True,blank=True)
    Email = models.CharField(max_length=64,default='',null=True,blank=True)
    Website = models.CharField(max_length=64,default='',null=True,blank=True)
    CoVatNo = models.CharField(max_length=15,default='',null=True,blank=True)
    CoRegNo = models.CharField(max_length=20,default='',null=True,blank=True)
    Entered = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    XeroContactID = models.CharField(default='',max_length=64,null=True,db_index=True)
    XeroUpdateFail = models.BooleanField(default=False,db_index=True)
    

    def __str__(self):
        return self.Code+': '+self.Name

class Contact(models.Model):
    ContactNumber = models.IntegerField(default=0,blank=False)
    RecordCode = models.CharField(max_length=10,default='',blank=False)
    RecordType = models.CharField(max_length=20,default='',blank=True)
    ContactType = models.CharField(max_length=20,default='',blank=True)
    Name = models.CharField(max_length=100,default='',blank=True)
    Phone = models.CharField(max_length=20,default='',blank=True)
    Mobile = models.CharField(max_length=20,default='',blank=True)
    Email = models.CharField(max_length=64,default='',blank=True)
    CCEmail = models.CharField(max_length=64,default='',blank=True)
    Address = models.TextField(max_length=160,default='',null=True,blank=True)
    Town = models.CharField(max_length=20,default='',blank=True)
    County = models.CharField(max_length=20,default='',blank=True)    
    PostCode = models.CharField(max_length=12,null=True,default='',blank=True)
    Country = models.CharField(max_length=20,default='',blank=True)
    EnteredBy = models.ForeignKey(User,'None')
    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code+': '+self.Name

class Item(models.Model):
    Code = models.CharField(unique=True,max_length=10,default='',blank=False)
    Name = models.CharField(max_length=100,default='',blank=True)
    SalesPrice = models.DecimalField(max_digits=20, decimal_places=2)
    CostPrice = models.DecimalField(max_digits=20, decimal_places=2)
    Entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code+': '+self.Name

class Analysis(models.Model):
    Code = models.CharField(unique=True,max_length=10,default='',blank=False)
    Name = models.CharField(max_length=100,default='',blank=True)
    Entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code+': '+self.Name

class VAT(models.Model):
    Code = models.CharField(unique=True,max_length=10,default='',blank=False)
    Name = models.CharField(max_length=100,default='',blank=True)
    VATRate = models.FloatField()
    Entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code

class SoHeader(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.DO_NOTHING) 
    date = models.DateTimeField(auto_now=True)
    order_date = models.DateField(default=datetime.date.today)
    required_date = models.DateField(default=datetime.date.today)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    account = models.CharField(default='',null=True,blank=True,max_length=10)
    SONumber = models.PositiveIntegerField()
    SOReference = models.CharField(default='',null=True,blank=True,max_length=20)    
    SOCurrency = models.ForeignKey(Currency,on_delete=models.DO_NOTHING, related_name = 'tocurrency',default='',null=True)
    SOCurrencycode = models.CharField(default='',null=True,blank=True,max_length=3)
    SOExRate = models.FloatField(default=1,null=True)
    SODescription = models.CharField(default='',null=True,blank=True,max_length=160)

    def __str__(self):
        return self.account+': '+str(self.SONumber)+': '+str(self.order_date)

# Create your models here.
class SoDetail2(models.Model):
    soheader = models.ForeignKey(SoHeader,on_delete=models.DO_NOTHING, related_name = 'tosoheader') 
    account = models.CharField(default='',null=True,blank=True,max_length=10)
    SONumber = models.PositiveIntegerField(default=0,null=True)
    SOLineNumber = models.PositiveIntegerField(default=0)
    item=models.ForeignKey(Item,on_delete=models.DO_NOTHING, related_name = 'toitem')
    itemcode = models.CharField(default='',null=True,blank=True,max_length=10)
    SODetail = models.TextField(default='',null=True,blank=True,max_length=240)
    SOQty = models.FloatField(default=0,null=True)
    SOSalesPrice = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    SONet = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    SOVat = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    SOHomeNet = models.DecimalField(default=0,max_digits=20, decimal_places=2)
    analysis=models.ForeignKey(Analysis,on_delete=models.DO_NOTHING, related_name = 'toanalysis') 
    analysiscode = models.CharField(default='',null=True,blank=True,max_length=10)
    vat=models.ForeignKey(VAT,on_delete=models.DO_NOTHING,null=True,blank=True, related_name = 'tovat')
    vatcode = models.CharField(default='',null=True,blank=True,max_length=10)


class CustomInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet, self).__init__(*args, **kwargs)
    def clean(self):
        super(CustomInlineFormSet, self).clean()
        # example custom validation across forms in the formset
    def get_extra(self, request, obj=None, **kwargs):
        return 0


class XeroPayments(models.Model):
    PaymentID = models.CharField(default='',null=True,blank=True,max_length=64)
    Date = models.DateTimeField(auto_now=True)
    BankAmount=models.FloatField(default=0)
    Amount=models.FloatField(default=0)
    Reference = models.CharField(default='',null=True,blank=True,max_length=20)
    CurrencyRate=models.FloatField(default=1,null=True)
    PaymentType = models.CharField(default='',null=True,blank=True,max_length=20)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    UpdatedDateUTC = models.DateTimeField(auto_now=True)
    IsReconciled = models.BooleanField(default=False)
    AnalysisCode = models.CharField(default='',null=True,blank=True,max_length=10)
    RowUpdated = models.DateTimeField(auto_now=True)
    RowInserted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.PaymentID+': '+str(self.Date)+': '+str(self.Amount)

class XeroPaymentsInvoice(models.Model):   
    ContactID = models.CharField(default='',null=True,blank=True,max_length=64)
    ContactName = models.CharField(default='',null=True,blank=True,max_length=100)
    CurrencyCode = models.CharField(default='',null=True,blank=True,max_length=10)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    InvoiceID = models.CharField(default='',null=True,blank=True,max_length=64)
    InvoiceNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    PaymentID = models.CharField(default='',null=True,blank=True,max_length=64)
    RowUpdated = models.DateTimeField(auto_now=True)
    RowInserted = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('InvoiceID', 'PaymentID',)

    def __str__(self):
        return self.InvoiceID+': '+str(self.InvoiceNumber)+': '+str(self.CurrencyCode)

class XeroOverPayments(models.Model):
    ContactID = models.CharField(default='',null=True,blank=True,max_length=64)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(auto_now=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(default='',null=True,blank=True,max_length=20)
    SubTotal=models.FloatField(default=0)
    TotalTax=models.FloatField(default=0)
    Total=models.FloatField(default=0)
    UpdatedDateUTC = models.DateTimeField(auto_now=True)
    CurrencyCode = models.CharField(default='',null=True,blank=True,max_length=4)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    RemainingCredit=models.FloatField(default=0)
    HasAttachments = models.BooleanField(default=False)
    OverpaymentID = models.CharField(default='',null=True,blank=True,max_length=64)
    RowUpdated = models.DateTimeField(auto_now=True)
    RowInserted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.OverpaymentID

class XeroPrePayments(models.Model):
    ContactID = models.CharField(default='',null=True,blank=True,max_length=64)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(auto_now=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(default='',null=True,blank=True,max_length=20)
    SubTotal=models.FloatField(default=0)
    TotalTax=models.FloatField(default=0)
    Total=models.FloatField(default=0)
    UpdatedDateUTC = models.DateTimeField(auto_now=True)
    CurrencyCode = models.CharField(default='',null=True,blank=True,max_length=4)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    Reference = models.CharField(default='',null=True,blank=True,max_length=50)
    RemainingCredit=models.FloatField(default=0)
    HasAttachments = models.BooleanField(default=False)
    PrepaymentID = models.CharField(default='',null=True,blank=True,max_length=64)
    RowUpdated = models.DateTimeField(auto_now=True)
    RowInserted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.OverpaymentID

class XeroSOInvLink(models.Model):
    InvoiceID = models.CharField(default='',null=True,blank=True,max_length=64)
    InvoiceNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    SOID = models.PositiveIntegerField()
    SONumber = models.PositiveIntegerField()
    Code = models.CharField(default='',null=True,blank=True,max_length=10)
    RowUpdated = models.DateTimeField(auto_now=True)
    RowInserted = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('InvoiceID', 'SOID',)

    def __str__(self):
        return self.OverpaymentID

class XeroInvoices(models.Model):
    ContactID = models.CharField(default='',null=True,blank=True,max_length=64)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(auto_now=True)
    DueDate = models.DateTimeField(auto_now=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(default='',null=True,blank=True,max_length=20)
    SubTotal=models.FloatField(default=0)
    TotalTax=models.FloatField(default=0)
    Total=models.FloatField(default=0)
    UpdatedDateUTC = models.DateTimeField(auto_now=True)
    CurrencyCode = models.CharField(default='',null=True,blank=True,max_length=4)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    InvoiceID = models.CharField(default='',null=True,blank=True,max_length=64)
    InvoiceNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    AmountDue=models.FloatField(default=0)
    AmountPaid=models.FloatField(default=0)
    AmountCredited=models.FloatField(default=0)
    CurrencyRate=models.FloatField(default=1,null=True)
    HasAttachments = models.BooleanField(default=False)
    def __str__(self):
        return self.InvoiceID+': '+str(self.Date)+': '+str(self.Total)

class XeroCreditNotes(models.Model):
    ContactID = models.CharField(default='',null=True,blank=True,max_length=64)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(auto_now=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(default='',null=True,blank=True,max_length=20)
    SubTotal=models.FloatField(default=0)
    TotalTax=models.FloatField(default=0)
    Total=models.FloatField(default=0)
    UpdatedDateUTC = models.DateTimeField(auto_now=True)
    CurrencyCode = models.CharField(default='',null=True,blank=True,max_length=4)
    CurrencyRate=models.FloatField(default=1,null=True)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    Reference = models.CharField(default='',null=True,blank=True,max_length=50)
    RemainingCredit=models.FloatField(default=0)
    HasAttachments = models.BooleanField(default=False)
    CreditNoteID = models.CharField(default='',null=True,blank=True,max_length=64)
    CreditNoteNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    def __str__(self):
        return self.CreditNoteID+': '+str(self.Date)+': '+str(self.Total)

class XeroAllInvoices(models.Model):
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    ContactID = models.CharField(default='',blank=True,max_length=64)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(null=True,)
    DueDate = models.DateTimeField(null=True,)
    Status = models.CharField(null=True,max_length=20)
    LineAmountTypes = models.CharField(null=True,max_length=20)

    SubTotal = models.FloatField(default=0,null=True,)
    TotalTax = models.FloatField(default=0,null=True,)
    Total = models.FloatField(default=0,null=True,)
    TotalDiscount = models.FloatField(default=0,null=True,)
    UpdatedDateUTC = models.DateTimeField(null=True,)
    CurrencyCode = models.CharField(null=True,blank=True,max_length=4)
    CurrencyRate = models.FloatField(default=1,null=True,)
    InvoiceID = models.CharField(default='',max_length=64)
    InvoiceNumber = models.CharField(default='',max_length=50)

    Reference = models.CharField(default='',null=True,blank=True,max_length=50)
    BrandingThemeID = models.CharField(default='',null=True,blank=True,max_length=64)
    Url = models.CharField(default='',null=True,blank=True,max_length=100)
    SentToContact = models.BooleanField(default=False,)
    ExpectedPaymentDate = models.DateTimeField(null=True,)
    PlannedPaymentDate = models.DateTimeField(null=True,)
    HasAttachments = models.BooleanField(default=False,)




    AmountDue = models.FloatField(default=0,null=True,)
    AmountPaid = models.FloatField(default=0,null=True,)
    CISDeduction = models.FloatField(default=0,null=True,)
    FullyPaidOnDate = models.DateTimeField(null=True,)
    AmountCredited = models.FloatField(default=0,null=True,)

    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.InvoiceID+': '+str(self.Date)+': '+str(self.Total)


class XeroAllCreditNotes(models.Model):
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    ContactID = models.CharField(default='',blank=True,max_length=64)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(null=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(null=True,max_length=20)

    SubTotal = models.FloatField(default=0,null=True)
    TotalTax = models.FloatField(default=0,null=True)
    Total = models.FloatField(default=0,null=True)

    CISDeduction = models.FloatField(default=0,null=True)
    UpdatedDateUTC = models.DateTimeField(null=True)
    CurrencyCode = models.CharField(null=True,blank=True,max_length=4)
    FullyPaidOnDate = models.DateTimeField(null=True)
    CreditNoteID = models.CharField(default='',null=True,blank=True,max_length=64)
    CreditNoteNumber = models.CharField(default='',max_length=50)

    Reference = models.CharField(default='',max_length=50)
    SentToContact = models.BooleanField(default=False)
    CurrencyRate = models.FloatField(default=1,null=True)


    RemainingCredit = models.FloatField(default=0,null=True)

    BrandingThemeID = models.CharField(default='',null=True,blank=True,max_length=64)
    HasAttachments = models.BooleanField(default=False)

    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.CreditNoteID+': '+str(self.Date)+': '+str(self.Total)

class XeroAllPayments(models.Model):
    PaymentID = models.CharField(default='',blank=True,max_length=64)
    AccountID = models.CharField(default='',blank=True,max_length=64)
    Code = models.CharField(null=True,blank=True,max_length=20)
    Date = models.DateTimeField(null=True)
    CurrencyRate = models.FloatField(default=1,null=True)
    BankAmount = models.FloatField(default=0,null=True)
    Amount = models.FloatField(default=0,null=True)
    Reference = models.CharField(default='',max_length=50)
    IsReconciled = models.BooleanField(default=False)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    PaymentType = models.CharField(null=True,blank=True,max_length=20)
    UpdatedDateUTC = models.DateTimeField(null=True)
    Code = models.CharField(default='',null=True,blank=True,max_length=20)
    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.PaymentID+': '+str(self.Date)+': '+str(self.Amount)

class XeroAllOverPayments(models.Model):
    ContactID = models.CharField(default='',blank=True,max_length=64)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    Date = models.DateTimeField(null=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(null=True,max_length=20)
    SubTotal = models.FloatField(default=0,null=True)
    TotalTax = models.FloatField(default=0,null=True)
    Total = models.FloatField(default=0,null=True)
    UpdatedDateUTC = models.DateTimeField(null=True)
    CurrencyCode = models.CharField(null=True,blank=True,max_length=4)
    Type = models.CharField(null=True,max_length=20)
    RemainingCredit = models.FloatField(default=0,null=True)
    HasAttachments = models.BooleanField(default=False)
    OverpaymentID = models.CharField(default='',blank=True,max_length=64)
    CurrencyRate = models.FloatField(default=1,null=True)
    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.OverpaymentID

class XeroAllPrePayments(models.Model):
    ContactID = models.CharField(default='',blank=True,max_length=64)
    Name = models.CharField(default='',blank=True,max_length=64)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    Date = models.DateTimeField(null=True)
    Status = models.CharField(default='',null=True,blank=True,max_length=20)
    LineAmountTypes = models.CharField(null=True,max_length=20)
    SubTotal = models.FloatField(default=0,null=True)
    TotalTax = models.FloatField(default=0,null=True)
    Total = models.FloatField(default=0,null=True)
    UpdatedDateUTC = models.DateTimeField(null=True)
    CurrencyCode = models.CharField(null=True,blank=True,max_length=4)
    Type = models.CharField(null=True,max_length=20)
    RemainingCredit = models.FloatField(default=0,null=True)
    HasAttachments = models.BooleanField(default=False)
    PrepaymentID = models.CharField(default='',blank=True,max_length=64)
    CurrencyRate = models.FloatField(default=1,null=True)
    Reference = models.CharField(null=True,max_length=20)
    FullyPaidOnDate = models.DateTimeField(null=True)
    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.OverpaymentID

class XeroAllPaymentAnalysis(models.Model):   
    ContactID = models.CharField(default='',null=True,blank=True,max_length=64)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    CurrencyCode = models.CharField(default='',null=True,blank=True,max_length=10)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    ObjectID = models.CharField(default='',null=True,blank=True,max_length=64)
    ObjectNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    PaymentID = models.CharField(default='',null=True,blank=True,max_length=64)
    RowUpdated = models.DateTimeField(auto_now=True)
    RowInserted = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('ObjectID', 'PaymentID',)

    def __str__(self):
        return self.ObjectID+': '+str(self.ObjectNumber)+': '+str(self.CurrencyCode)

class XeroAllContacts(models.Model):   
    ContactID = models.CharField(default='',blank=True,max_length=64)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    AccountNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    ContactStatus = models.CharField(default='',null=True,blank=True,max_length=20)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    FirstName = models.CharField(default='',null=True,blank=True,max_length=100)
    LastName = models.CharField(default='',null=True,blank=True,max_length=100)
    EmailAddress = models.CharField(default='',null=True,blank=True,max_length=64)
    SkypeUserName = models.CharField(default='',null=True,blank=True,max_length=100)
    BankAccountDetails = models.CharField(default='',null=True,blank=True,max_length=50)
    TaxNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    AccountsReceivableTaxType = models.CharField(default='',null=True,blank=True,max_length=20)
    AccountsPayableTaxType = models.CharField(default='',null=True,blank=True,max_length=20)
    IsSupplier = models.BooleanField(default=False)
    IsCustomer = models.BooleanField(default=False)
    DefaultCurrency = models.CharField(default='',null=True,blank=True,max_length=4)
    UpdatedDateUTC = models.DateTimeField(null=True)

    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.ContactID+': '+str(self.ContactNumber)+': '+str(self.AccountNumber)


class XeroAllContactPersons(models.Model):   
    ContactID = models.CharField(default='',null=True,blank=True,max_length=100)
    FirstName = models.CharField(default='',null=True,blank=True,max_length=100)
    LastName = models.CharField(default='',null=True,blank=True,max_length=100)
    EmailAddress = models.CharField(default='',null=True,blank=True,max_length=64)
    IncludeInEmails = models.BooleanField(default=False)

    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.ContactID+': '+str(self.EmailAddress)

class XeroAllAddresses(models.Model):   
    ContactID = models.CharField(default='',blank=True,max_length=64)
    AddressType = models.CharField(default='',null=True,blank=True,max_length=20)
    AddressLine1 = models.CharField(default='',null=True,blank=True,max_length=160)
    AddressLine2 = models.CharField(default='',null=True,blank=True,max_length=160)
    AddressLine3 = models.CharField(default='',null=True,blank=True,max_length=160)
    AddressLine4 = models.CharField(default='',null=True,blank=True,max_length=160)
    City = models.CharField(default='',null=True,blank=True,max_length=100)
    Region = models.CharField(default='',null=True,blank=True,max_length=100)
    PostalCode = models.CharField(default='',null=True,blank=True,max_length=12)
    Country = models.CharField(default='',null=True,blank=True,max_length=20)
    AttentionTo = models.CharField(default='',null=True,blank=True,max_length=100)


    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ContactID', 'AddressType',)


    def __str__(self):
        return self.ContactID+': '+str(self.AddressType)+': '+str(self.PostalCode)

class XeroAllTaxRates(models.Model):   
    Name = models.CharField(unique=True,default='',blank=True,max_length=100)
    TaxType = models.CharField(default='',blank=True,max_length=20)
    CanApplyToAssets = models.BooleanField(default=False)
    CanApplyToEquity = models.BooleanField(default=False)
    CanApplyToExpenses = models.BooleanField(default=False)
    CanApplyToLiabilities = models.BooleanField(default=False)
    CanApplyToRevenue = models.BooleanField(default=False)
    DisplayTaxRate = models.FloatField(default=0,null=True)
    EffectiveRate = models.FloatField(default=0,null=True)
    Status = models.CharField(default='',blank=True,max_length=20)

    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ContactID+': '+str(self.Name)+': '+str(self.DisplayTaxRate)

class XeroAllAccounts(models.Model):   
    Code = models.CharField(unique=True,default='',blank=True,max_length=30)
    Name = models.CharField(default='',blank=True,max_length=100)
    Type = models.CharField(default='',blank=True,max_length=20)
    BankAccountNumber = models.CharField(default='',blank=True,max_length=30)
    Status = models.CharField(default='',blank=True,max_length=20)
    Description = models.CharField(default='',blank=True,max_length=1000)
    BankAccountType = models.CharField(default='',blank=True,max_length=20)
    CurrencyCode = models.CharField(default='',blank=True,max_length=4)
    TaxType = models.CharField(default='',blank=True,max_length=20)
    EnablePaymentsToAccount = models.BooleanField(default=False)
    ShowInExpenseClaims = models.BooleanField(default=False)
    AccountID = models.CharField(unique=True,default='',blank=True,max_length=64)
    Class = models.CharField(default='',blank=True,max_length=20)
    SystemAccount = models.BooleanField(default=False)
    ReportingCode = models.CharField(default='',blank=True,max_length=100)
    ReportingCodeName = models.CharField(default='',blank=True,max_length=100)
    HasAttachments = models.BooleanField(default=False)
    UpdatedDateUTC = models.DateTimeField(null=True)


    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ContactID+': '+str(self.Name)+': '+str(self.DisplayTaxRate)

class XeroAllCurrencies(models.Model):   
    Code = models.CharField(unique=True,default='',blank=True,max_length=4)    
    Description = models.CharField(default='',blank=True,max_length=240) 
    
    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code+': '+str(self.Description)

class XeroAllItems(models.Model):   
    ItemID = models.CharField(unique=True,default='',blank=True,max_length=64)
    Code = models.CharField(unique=True,default='',blank=True,max_length=50)
    Name = models.CharField(default='',blank=True,max_length=100)
    IsSold = models.BooleanField(default=False)
    IsPurchased = models.BooleanField(default=False)
    Description = models.CharField(default='',blank=True,max_length=1000)
    PurchaseDescription = models.CharField(default='',blank=True,max_length=1000)
    IsTrackedAsInventory = models.BooleanField(default=False)
    InventoryAssetAccountCode = models.CharField(default='',blank=True,max_length=50)
    TotalCostPool = models.FloatField(default=0,null=True)
    QuantityOnHand = models.FloatField(default=0,null=True)
    UpdatedDateUTC = models.DateTimeField(null=True)
    CostUnitPrice = models.FloatField(default=0,null=True)
    CostAccountCode = models.CharField(default='',blank=True,max_length=50)
    COGSAccountCode = models.CharField(default='',blank=True,max_length=50)
    CostTaxType = models.CharField(default='',blank=True,max_length=20)
    SalesUnitPrice = models.FloatField(default=0,null=True)
    SalesAccountCode = models.CharField(default='',blank=True,max_length=50)
    SalesTaxType = models.CharField(default='',blank=True,max_length=20)


    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Code+': '+str(self.Name)

class XeroAllCreditNoteAllocations(models.Model):
    CreditNoteID = models.CharField(default='',blank=True,max_length=64)
    CreditNoteNumber = models.CharField(default='',null=True,blank=True,max_length=50)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    ContactName = models.CharField(default='',null=True,blank=True,max_length=100)
    InvoiceID = models.CharField(default='',blank=True,max_length=64)
    InvoiceNumber = models.CharField(default='',null=True,blank=True,max_length=50)  
    Amount = models.FloatField(default=0,null=True)
    Date = models.DateTimeField(null=True)
    
    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Code+': '+str(self.Description)

class XeroAllJournals(models.Model):
    JournalID = models.CharField(default='',blank=True,max_length=64)
    JournalDate = models.DateTimeField(null=True)
    JournalNumber = models.CharField(default='',blank=True,max_length=50)
    CreatedDateUTC = models.DateTimeField(null=True)
    Reference = models.CharField(default='',blank=True,max_length=50)
    SourceID = models.CharField(default='',blank=True,max_length=64)
    SourceType = models.CharField(default='',blank=True,max_length=20)


    JournalLineID = models.CharField(unique=True,default='',blank=True,max_length=64)
    AccountID = models.CharField(default='',blank=True,max_length=64)
    AccountCode = models.CharField(default='',blank=True,max_length=50)
    AccountType = models.CharField(default='',blank=True,max_length=20)
    AccountName = models.CharField(default='',blank=True,max_length=100)
    Description = models.CharField(default='',blank=True,max_length=1000)
    NetAmount = models.FloatField(default=0,null=True)
    GrossAmount = models.FloatField(default=0,null=True)
    TaxAmount = models.FloatField(default=0,null=True)
    TaxType = models.CharField(default='',blank=True,max_length=50)
    TaxName = models.CharField(default='',blank=True,max_length=100)
    TrackingCategoryID = models.CharField(default='',blank=True,max_length=64,null=True)
    CategoryName = models.CharField(default='',blank=True,max_length=50,null=True)
    TrackingOptionID = models.CharField(default='',blank=True,max_length=64,null=True)
    OptionName = models.CharField(default='',blank=True,max_length=50,null=True)
    Status = models.CharField(default='',blank=True,max_length=20,null=True)

    Updated = models.DateTimeField(auto_now=True)
    Created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.JournalID

class XeroTranView(models.Model):
    id = models.IntegerField(default=0,primary_key=True)
    Type = models.CharField(default='',null=True,blank=True,max_length=20)
    TRANTYPE = models.CharField(default='',null=True,blank=True,max_length=10)
    ContactNumber = models.CharField(default='',null=True,blank=True,max_length=10)
    Name = models.CharField(default='',null=True,blank=True,max_length=100)
    Date = models.DateTimeField(null=True)
    SubTotal = models.FloatField(default=0,null=True)
    TotalTax = models.FloatField(default=0,null=True)
    Total = models.FloatField(default=0,null=True)
    CurrencyCode = models.CharField(null=True,max_length=4)
    CurrencyRate = models.FloatField(default=1,null=True)
    InvoiceNumber = models.CharField(null=True,max_length=20)
    Reference = models.CharField(null=True,max_length=20)
    AmountDue = models.FloatField(default=0,null=True)
    AmountPaid = models.FloatField(default=0,null=True)
    UpdatedDateUTC = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table='r21_vw_XeroTransactions'





