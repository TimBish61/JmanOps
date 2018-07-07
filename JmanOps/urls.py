"""
Definition of urls for JmanOps.
"""

from datetime import datetime
from django.conf.urls import include, url
import django.contrib.auth.views
import app.forms
import app.views
from django.contrib import admin





# Uncomment the next lines to enable the admin:
#from django.conf.urls import include
#from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^contact-list$', app.views.ContactList),
    url(r'^currency-list$', app.views.CurrencyList, name='currency-list'),
    url(r'^UpdateCurrencyTable$', app.views.UpdateCurrencyTable, name='UpdateCurrencyTable'),
    url(r'contact-edit/(?P<pk>[0-9]+)/$', app.views.ContactUpdateView.as_view(), name='contact-edit'),
    url(r'^contact-create/$', app.views.ContactCreateView.as_view(), name='contact-create'),
    url(r'contact-save-edit/$', app.views.contact_edit, name='contact-save-edit'),
    url(r'contact-delete/$', app.views.delete_contact, name='contact-delete'),
    url(r'^create_contactPost/$', app.views.add_new_contact_view),
    url(r'^search/', app.views.customer_search),
    url(r'^lookup/', app.views.customer_lookup),

    url(r'^order2$', app.views.order2.as_view(),name='order2'),
    url(r'^order-list$', app.views.OrderList,name='order-list'),
    url(r'order/(?P<pk>[0-9]+)/$', app.views.SOrderUpdate.as_view(), name='order-update'),
    url(r'order-delete/(?P<pk>[0-9]+)/delete/$', app.views.SOrderDelete, name='order-delete'),
    url(r'order-print/(?P<pk>[0-9]+)/$', app.views.CreatePdfTestView, name='order-print'),
    url(r'order-docprint/(?P<pk>[0-9]+)/$', app.views.write_pdf_view_doc, name='order-docprint'),
    url(r'^setcurrency/$', app.views.setCurrency,name='setcurrency'),
    url(r'^setXRate/$', app.views.setCurrencyRate,name='setXRate'),
    #needed for edit of order to get ajax script to work
    url(r'^order/\d/setcurrency/$', app.views.setCurrency,name='setcurrency'),
    url(r'^order/\d/setXRate/$', app.views.setCurrencyRate,name='setXRate'),

    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.home, name='contact'),
    url(r'^about', app.views.home, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    

    url(r'^customer$', app.views.CustomerView.as_view(), name='customer'),
    url(r'^search/', app.views.customer_search),
    url(r'^customer_move/$', app.views.customer_move),
    url(r'^customer_trans/$', app.views.customer_trans),
    #url(r'^customer_move/$', app.views.CustomerMoveView.as_view(), name='customer_move'),
    url(r'^create_custpost/$', app.views.create_custpost),
    url(r'^delete_customer/$', app.views.delete_customer),

    url(r'^getXeroPayments/$', app.views.get_Xero_Receipts, name='getXeroPayments'),
    url(r'^XeroInvoice/(?P<pk>[0-9]+)/$', app.views.add_Xero_invoice, name='XeroInvoice'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
]
