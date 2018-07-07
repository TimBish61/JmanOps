
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm


from app.models import SoHeader, SoDetail2, Currency, SYSTEM_MAIN, SYSTEM_BANK

try:
    from django.utils import importlib
except ImportError:
    import importlib

from django.shortcuts import get_object_or_404

#from django.conf import settings
from JmanOps.InvoiceSettings import settings, INV_LOGO
#from app.OrderPdf import draw_header
#from django.utils import format_currency
import datetime
from django.db.models import Sum



def draw_header(canvas):
    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(18 * cm, -1 * cm, 'Invoice')
    canvas.drawInlineImage(INV_LOGO, 1 * cm, -1 * cm, 25, 25)
    canvas.setLineWidth(4)
    canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)



def draw_address(canvas):
    """ Draws the business address """

    #oCompany=SYSTEM_MAIN.objects.filter(Name__contains=search_text)

    oCompany=get_object_or_404(SYSTEM_MAIN, pk=1)
    #business_details = (u''+oCompany.CompanyName+'',u''+ oCompany.Address +'')
    business_details = (
        u''+ oCompany.CompanyName +'',
        u''+ oCompany.Address +'',
        u''+ oCompany.Town +'',
        U''+ oCompany.County +'',
        U''+ oCompany.PostCode +'',
        U''+ oCompany.Country +'',
        u'',
        u'',
        u'Phone: '+ oCompany.Phone +'',
        u'Email: '+ oCompany.Email +'',
        u'Website: '+ oCompany.Website +'',
        u'VAT No: '+ oCompany.CoVatNo +'',
        u'Reg No:'+ oCompany.CoRegNo +''
    )
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(13 * cm, -2.5 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def draw_footer(canvas):
    """ Draws the invoice footer """
    oBank=get_object_or_404(SYSTEM_BANK, pk=1)
    oCompany=get_object_or_404(SYSTEM_MAIN, pk=1)
    oCompany=get_object_or_404(SYSTEM_MAIN, pk=1)
    note = (
        u'Bank Details: '+oBank.BankName+'',
        u'Sort Code: '+oBank.BankSortCode+' Account No: '+oBank.BankAccountNo+' (Quote invoice number).',
        u"Please pay via bank transfer or cheque. All payments should be made in "+oBank.Curency.Name+"'s.",
        u'Make cheques payable to '+oCompany.CompanyName+'.',
    )
    textobject = canvas.beginText(1 * cm, -27 * cm)
    for line in note:
        textobject.textLine(line)
    canvas.drawText(textobject)

def draw_pdf(buffer, invoice):
    """ Draws the invoice """
    canvas = Canvas(buffer, pagesize=A4)
    canvas.translate(0, 29.7 * cm)
    canvas.setFont('Helvetica', 10)

    canvas.saveState()
    draw_header(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_footer(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_address(canvas)
    canvas.restoreState()

    # Client address
    textobject = canvas.beginText(1.5 * cm, -2.5 * cm)
    #if invoice.address.contact_name:
    #    textobject.textLine(invoice.address.contact_name)
    textobject.textLine(invoice.customer.Name)
    addresslines=invoice.customer.Address.split('\r\n')
    for addressline in addresslines:
        textobject.textLine(addressline)
    #textobject.textLine(invoice.customer.Address.replace('\r\n','<br />\n'))
    if invoice.customer.Town:
        textobject.textLine(invoice.customer.Town)
    if invoice.customer.County:
        textobject.textLine(invoice.customer.County)
    textobject.textLine(invoice.customer.PostCode)
    textobject.textLine(invoice.customer.Country)
    canvas.drawText(textobject)


    #OrderLineCount=45
    oOrderLines=SoDetail2.objects.filter(soheader=invoice.id).order_by('SOLineNumber')
    OrderLineCount=oOrderLines.count()
    SumOrderNet=oOrderLines.aggregate(Sum('SONet'))
    SumOrderNet=SumOrderNet['SONet__sum']
    SumOrderVat=oOrderLines.aggregate(Sum('SOVat'))
    SumOrderVat=SumOrderVat['SOVat__sum']
    SumOrderGross=SumOrderNet+SumOrderVat
    #SumOrderNet=SoDetail2.objects.filter(SONet__isnull=True).aggregate(Sum('SONet'))
    pageLineCount=20
    pageCount=1+(OrderLineCount//pageLineCount) # floor division so returns whole number
    #lastpagelineCount=OrderLineCount%pageLineCount
    #make 30 lines
    lineStart=1

    for j in range(1, pageCount+1):#page loop

        if(j>1):
            canvas.translate(0, 29.7 * cm)
        canvas.setFont('Helvetica', 10)
        # Info

        textobject = canvas.beginText(1.5 * cm, -6.5 * cm)
        textobject.textLine(u'Invoice ID:')
        textobject.textLine(u'Invoice Date:')
        textobject.textLine(u'Client:')
        canvas.drawText(textobject)

        textobject = canvas.beginText(4.0 * cm, -6.5 * cm)
        textobject.textLine(u''+str(invoice.SONumber))
        textobject.textLine(u''+"{:%d %b %Y}".format(invoice.order_date))
        textobject.textLine(u''+invoice.customer.Code+': ' + invoice.customer.Name)
        canvas.drawText(textobject)

        lineStart=((j-1)*pageLineCount)+1
        
        if(j!=pageCount):
            lineEnd=lineStart+pageLineCount
        else:#last page
            lineEnd=OrderLineCount+1

        data = None
        data = [[u'Description', u'Quantity', u'Price '+invoice.SOCurrency.Symbol, u'Total '+invoice.SOCurrency.Symbol], ]  


        for i in range(lineStart,lineEnd):             

            data.append([
                '#'+str(oOrderLines[i-1].SOLineNumber)+' '+oOrderLines[i-1].SODetail,
                "{:.1f}".format(oOrderLines[i-1].SOQty),
                "{:,.2f}".format(oOrderLines[i-1].SOSalesPrice),
                "{:,.2f}".format(oOrderLines[i-1].SONet)
                ])
   
        table=None
        tableTotal=None
        table = Table(data, colWidths=[11 * cm, 2 * cm, 3 * cm, 3 * cm])
        
        
        if(j==1):
            table.setStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
                ('ALIGN', (-3, 0), (-1, -1), 'RIGHT'),
                ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            ])
            tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
            table.drawOn(canvas, 1 * cm, -8 * cm - th)
        elif(j!=pageCount):#normal pages - not 1st or last
            table.setStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
                ('ALIGN', (-3, 0), (-1, -1), 'RIGHT'),
                ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            ])
            tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
            table.drawOn(canvas, 1 * cm, -8 * cm - th)
        elif(j==pageCount):# last page
            table.setStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
                ('ALIGN', (-3, 0), (-1, -1), 'RIGHT'),
                ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
            ])
            tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
            table.drawOn(canvas, 1 * cm, -8 * cm - th)

            #datatotal = [[u'Description', u'Quantity', u'Price '+invoice.SOCurrency.Symbol, u'Total '+invoice.SOCurrency.Symbol], ]
            datatotal=[[u'', u'', u'Net '+invoice.SOCurrency.Symbol+':', u''+str("{:,.2f}".format(SumOrderNet))]]
            datatotal.append([u'', u'', u'VAT '+invoice.SOCurrency.Symbol+':', u''+str("{:,.2f}".format(SumOrderVat))])
            datatotal.append([u'', u'', u'Total '+invoice.SOCurrency.Symbol+':', u''+str("{:,.2f}".format(SumOrderGross))])

            tableTotal = Table(datatotal, colWidths=[11 * cm, 2 * cm, 3 * cm, 3 * cm])
            tableTotal.setStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                ('GRID', (2, 0), (3, -1), 1, (0.7, 0.7, 0.7)),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
             ])
            tw, th, = tableTotal.wrapOn(canvas, 15 * cm, 19 * cm)
            tableTotal.drawOn(canvas, 1 * cm, -24.75 * cm)

        canvas.drawString(17 * cm, - 28.7 * cm, "Page " + str(j) + " of "+ str(pageCount))
        
        canvas.showPage()#each page

    canvas.save()
