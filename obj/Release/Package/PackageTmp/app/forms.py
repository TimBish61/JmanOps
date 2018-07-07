"""
Definition of forms.
"""

from crispy_forms.helper import FormHelper


from app.models import Customer,Contact,SoHeader, SoDetail2, Item, VAT, Analysis, Currency,CustomInlineFormSet
from django.forms import ModelForm, inlineformset_factory
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class CustomerForm(forms.ModelForm):  
    
    helper = FormHelper()
    helper.form_show_labels=False



    id=forms.CharField(max_length=10,
                            widget=forms.HiddenInput({
                                'id': 'post-id',
                                'class': 'form-control',
                                'placeholder': 'id'}))
    Code = forms.CharField(max_length=10,
                               widget=forms.TextInput({
                                   'id': 'post-Code',
                                   'class': 'form-control',
                                   'placeholder': 'Code'}))
    Name = forms.CharField(max_length=100,required=False,
                               widget=forms.TextInput({
                                   'id': 'post-Name',
                                   'class': 'form-control',
                                   'placeholder': 'Name'}))
    Address = forms.CharField(max_length=240,required=False,widget=forms.Textarea({
                                    'id': 'post-Address',
                                    'class': 'form-comtrol',
                                   'placeholder': 'Address'}))
    PostCode = forms.CharField(max_length=12,required=False,
                               widget=forms.TextInput({
                                   'id': 'post-PostCode',
                                   'class': 'form-control',
                                   'placeholder': 'Post Code'}))
    currency_code = forms.ModelChoiceField(queryset=Currency.objects.order_by('Code'),
                               widget=forms.Select(attrs={'id':'post-currency_code'}))
    #Entered = forms.DateField()
    
    class Meta:
        model = Customer
        fields = ('id','Code','Name','Address','PostCode','currency_code',)


class ContactForm(forms.ModelForm):  
    
    helper = FormHelper()
    helper.form_show_labels=False



    id=forms.CharField(max_length=10,
                            widget=forms.HiddenInput({
                                'id': 'con-id',
                                'class': 'form-control',
                                'placeholder': 'id'}))
    #ContactNumber = forms.IntegerField(widget=forms.NumberInput({
    #                               'id': 'con-ContactNumber',
    #                               'class': 'form-control',
    #                               'placeholder': 'Number'}))
    #RecordCode = forms.CharField(widget=forms.HiddenInput())
    #RecordCode = forms.CharField(max_length=10,
    #                           widget=forms.HiddenInput({
    #                               'id': 'con-RecordCode',
    #                               'class': 'form-control'}))
    #RecordType = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-RecordType',
    #                               'class': 'form-control',
    #                               'placeholder': 'Record Type'}))
    #ContactType = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-ContactType',
    #                               'class': 'form-control',
    #                               'placeholder': 'Contact Type'}))
    Name = forms.CharField(max_length=100,required=False,
                               widget=forms.TextInput({
                                   'id': 'con-Name',
                                   'class': 'form-control',
                                   'placeholder': 'Name'}))
    #Phone = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-Phone',
    #                               'class': 'form-control',
    #                               'placeholder': 'Phone'}))
    Mobile = forms.CharField(max_length=20,
                               widget=forms.TextInput({
                                   'id': 'con-Mobile',
                                   'class': 'form-control',
                                   'placeholder': 'Mobile'}))
    Email = forms.CharField(max_length=64,
                               widget=forms.TextInput({
                                   'id': 'con-Email',
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
    #CCEmail = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-CCEmail',
    #                               'class': 'form-control',
    #                               'placeholder': 'CCEmail'}))
    #Address = forms.CharField(max_length=160,required=False,widget=forms.Textarea({
    #                                'id': 'con-Address',
    #                                'class': 'form-comtrol',
    #                               'placeholder': 'Address'}))
    #Town = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-Town',
    #                               'class': 'form-control',
    #                               'placeholder': 'Town'}))
    #County = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-County',
    #                               'class': 'form-control',
    #                               'placeholder': 'County'}))
    #PostCode = forms.CharField(max_length=12,required=False,
    #                           widget=forms.TextInput({
    #                               'id': 'con-PostCode',
    #                               'class': 'form-control',
    #                               'placeholder': 'Post Code'}))
    #Country = forms.CharField(max_length=20,
    #                           widget=forms.TextInput({
    #                               'id': 'con-Country',
    #                               'class': 'form-control',
    #                               'placeholder': 'Country'}))

    #ContactNumber = models.IntegerField(default=0,blank=False)
    #RecordCode = models.CharField(max_length=10,default='',blank=False)
    #RecordType = models.CharField(max_length=20,default='',blank=True)
    #ContactType = models.CharField(max_length=20,default='',blank=True)
    #Name = models.CharField(max_length=100,default='',blank=True)
    #Phone = models.CharField(max_length=20,default='',blank=True)
    #Mobile = models.CharField(max_length=20,default='',blank=True)
    #Email = models.CharField(max_length=64,default='',blank=True)
    #CCEmail = models.CharField(max_length=64,default='',blank=True)
    #Address = models.TextField(max_length=160,default='',null=True,blank=True)
    #Town = models.CharField(max_length=20,default='',blank=True)
    #County = models.CharField(max_length=20,default='',blank=True)    
    #PostCode = models.CharField(max_length=12,null=True,default='',blank=True)
    #Country = models.CharField(max_length=20,default='',blank=True)
    #EnteredBy = models.ForeignKey(User)
    #Updated = models.DateTimeField(auto_now=True)
    #Created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        model = Contact
        #fields = '__all__'
        #fields = ('id','ContactNumber','RecordCode','RecordType','ContactType','Name','Phone','Mobile','Email','CCEmail','Address','Town','County','PostCode','Country')
        fields = ('id','Name','Mobile','Email')

class ContactFormNew(forms.ModelForm):  
    
    helper = FormHelper()
    helper.form_show_labels=False



    #id=forms.CharField(max_length=10,
    #                        widget=forms.HiddenInput({
    #                            'id': 'con-id',
    #                            'class': 'form-control',
    #                            'placeholder': 'id'}))

    Name = forms.CharField(max_length=100,required=False,
                               widget=forms.TextInput({
                                   'id': 'con-Name',
                                   'class': 'form-control',
                                   'placeholder': 'Name'}))
    Mobile = forms.CharField(max_length=20,
                               widget=forms.TextInput({
                                   'id': 'con-Mobile',
                                   'class': 'form-control',
                                   'placeholder': 'Mobile'}))
    Email = forms.CharField(max_length=64,
                               widget=forms.TextInput({
                                   'id': 'con-Email',
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))

    
    class Meta:
        model = Contact
        #fields = '__all__'
        #fields = ('id','ContactNumber','RecordCode','RecordType','ContactType','Name','Phone','Mobile','Email','CCEmail','Address','Town','County','PostCode','Country')
        fields = ('Name','Mobile','Email')


class SoHeaderForm(forms.ModelForm):    
    class Meta:
        model=SoHeader
        fields = ['customer','order_date','required_date','SONumber','SOReference','SOCurrency', 'SOExRate','SODescription']
        #labels={'customer': 'customer','order_date': 'Date','required_date': 'Required','SONumber': 'Number','SOReference': 'Reference','SOExRate': 'Rate'}
    def __init__(self, *args, **kwargs):
        super(SoHeaderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].label="Customer"
        self.fields['order_date'].label="Date"
        self.fields['required_date'].label="Required"
        self.fields['SONumber'].disabled=True
        self.fields['SONumber'].label="Number"
        self.fields['SOReference'].label="Reference"        
        #self.fields['SOCurrency']=forms.ModelChoiceField(queryset=Currency.objects.order_by('Code'))
        self.fields['SOCurrency'].label="Currency"
        self.fields['SOExRate'].label="Rate"        
        self.fields['SODescription']=forms.CharField(max_length=160,widget=forms.TextInput(attrs={'size': '800'}))
        self.fields['SODescription'].label="Description"

class SoDetail2Form(forms.ModelForm):
    class Meta:
        model=SoDetail2
        #fields = ('Name','Mobile','Email')
        fields = ('SOLineNumber','SOQty','SOSalesPrice','SODetail','item','analysis','vat','SONet',)
    def __init__(self, *args, **kwargs):
            super(SoDetail2Form, self).__init__(*args, **kwargs)
            self.fields['account']=forms.CharField(max_length=10,widget=forms.HiddenInput(), initial='A')
            #needed tp prevent save error (form_isvalid()) when line added from script
            self.fields['account'].required = False 
            self.fields['SONumber']=forms.IntegerField(widget=forms.HiddenInput(), initial=0)
            self.fields['SONumber'].label="Order No"
            #needed tp prevent save error (form_isvalid()) when line added from script
            self.fields['SONumber'].required = False
            self.fields['SOLineNumber']=forms.IntegerField(initial=1,widget=forms.NumberInput({'style': 'text-align: right; width: 20px;'}))
            self.fields['SOLineNumber'].label="#"
            self.fields['SOLineNumber'].disabled=True
            self.fields['item']=forms.ModelChoiceField(queryset=Item.objects.order_by('?'))
            self.fields['item'].label="Title"
            self.fields['SODetail']=forms.CharField(max_length=240,widget=forms.Textarea(attrs={'rows':1, 'cols':30,'class': 'LineText'}))
            self.fields['SODetail'].label="Detail"
            self.fields['SOQty']=forms.FloatField(initial=1,widget=forms.NumberInput({'style': 'text-align: right; width: 80px;','class': 'soqty'}))
            self.fields['SOQty'].label="Qty"
            #self.fields['SOQty']=forms.FloatField(widget=forms.NumberInput({'class': 'soqty'}))
            self.fields['SOSalesPrice']=forms.DecimalField(widget=forms.NumberInput({'style': 'text-align: right; width: 80px;'}))
            self.fields['SOSalesPrice'].label="Price"
            self.fields['SONet']=forms.DecimalField(widget=forms.NumberInput({'style': 'text-align: right; width: 80px;'}))
            self.fields['SONet'].label="Net"
            self.fields['analysis']=forms.ModelChoiceField(queryset=Analysis.objects.order_by('?'))
            self.fields['analysis'].label="Analysis"
            
SoDetailFormSetNew = inlineformset_factory(SoHeader, SoDetail2,
                                            form=SoDetail2Form, extra=1)

SoDetailFormSetEdit = inlineformset_factory(SoHeader, SoDetail2,
                                            form=SoDetail2Form, extra=0)

class SOFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SOFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'favorite_color',
            'favorite_food',
        )
        self.render_required_fields = True



