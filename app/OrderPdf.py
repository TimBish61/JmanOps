from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from app.PageNumberdReport import PageNumCanvas

try:
    from django.utils import importlib
except ImportError:
    import importlib

#from django.conf import settings
from JmanOps.InvoiceSettings import settings, INV_LOGO
#from app.OrderPdf import draw_header
#from django.utils import format_currency
import datetime

def draw_header_test(canvas,w, h):
    #A$: 210 x 297 mm
#    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica', 16)
    canvas.drawString((w-2.1) * cm, (h-1) * cm, 'Invoice')
    canvas.drawInlineImage(INV_LOGO, 1 * cm, (h-1) * cm, 20, 20)
    canvas.setLineWidth(4)
    canvas.line(0, (h-1.25) * cm, h * cm, (h-1.25) * cm)


def draw_test(canvas):
    canvas.drawString(18*cm, 800, "Hello World")

#def draw_header(canvas,w,h):
#    #A$: 210 x 297 mm
##    """ Draws the invoice header """
#    canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
#    canvas.setFillColorRGB(0.2, 0.2, 0.2)
#    canvas.setFont('Helvetica', 16)
#    canvas.drawString((w-2.1) * cm, (h-1) * cm, 'Invoice')
#    canvas.drawInlineImage(INV_LOGO, 1 * cm, (h-1) * cm, 20, 20)
#    canvas.setLineWidth(4)
#    canvas.line(0, (h-1.25) * cm, h * cm, (h-1.25) * cm)
    

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
    business_details = (
        u'COMPANY NAME LTD',
        u'STREET',
        u'TOWN',
        U'COUNTY',
        U'POSTCODE',
        U'COUNTRY',
        u'',
        u'',
        u'Phone: +00 (0) 000 000 000',
        u'Email: example@example.com',
        u'Website: www.example.com',
        u'Reg No: 00000000'
    )
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(13 * cm, -2.5 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def draw_footer(canvas):
    """ Draws the invoice footer """
    note = (
        u'Bank Details: Street address, Town, County, POSTCODE',
        u'Sort Code: 00-00-00 Account No: 00000000 (Quote invoice number).',
        u'Please pay via bank transfer or cheque. All payments should be made in CURRENCY.',
        u'Make cheques payable to Company Name Ltd.',
    )
    textobject = canvas.beginText(1 * cm, -27 * cm)
    for line in note:
        textobject.textLine(line)
    canvas.drawText(textobject)


#inv_module = "Order.pdf"
#header_func = draw_header(canvas)
#address_func = draw_address(canvas)
#footer_func = draw_footer(canvas)

#INV_MODULE = getattr(settings, 'INV_MODULE', 'invoice.pdf')
#INV_LOGO = getattr(settings, 'INV_LOGO', path.join(settings.MEDIA_ROOT, 'static/images/logo.jpg'))
#INV_CURRENCY = getattr(settings, 'INV_CURRENCY', u'EUR')
#INV_CURRENCY_SYMBOL = getattr(settings, 'INV_CURRENCY_SYMBOL', u'€')
#INV_EMAIL_SUBJECT = getattr(settings, 'INV_EMAIL_SUBJECT', u'[%s] Invoice %%(invoice_id)s' % (settings.SITE_NAME))


def draw_pdf(buffer, invoice, canvasmaker=PageNumCanvas):
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
    #textobject.textLine(invoice.address.address_one)
    #if invoice.address.address_two:
    #    textobject.textLine(invoice.address.address_two)
    #textobject.textLine(invoice.address.town)
    #if invoice.address.county:
    #    textobject.textLine(invoice.address.county)
    #textobject.textLine(invoice.address.postcode)
    #textobject.textLine(invoice.address.country.name)


    textobject.textLine('Tim Bishop')
    textobject.textLine('Address Line 1')
    textobject.textLine('Address Line 2')
    textobject.textLine('Town')
    textobject.textLine('County')
    textobject.textLine('GU4 8RQ')
    textobject.textLine('UK')
    canvas.drawText(textobject)

    # Info
    textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
    #textobject.textLine(u'Invoice ID: %s' % invoice.invoice_id)
    textobject.textLine(u'Invoice ID: %s' % 12)
    textobject.textLine(u'Invoice Date: %s' % datetime.date.today())
    textobject.textLine(u'Client: %s' % 'Tim')
    canvas.drawText(textobject)

    #Test Lines
    Order = {}
    Order["OrderLines"] = []
    OrderLines = Order["OrderLines"]
    #OrderLine1 = {"quantity":2,"description":"Order Line 1","unit_price": 12,"total": 24}
    #OrderLine2 = {"quantity":4,"description":"Order Line 2","unit_price": 10,"total": 40}
    #OrderLine3 = {"quantity":6,"description":"Order Line 3","unit_price": 80,"total": 480}
    #OrderLines.append(OrderLine1)
    #OrderLines.append(OrderLine2)
    #OrderLines.append(OrderLine3)

    #make 30 lines
    for i in range(1,41):
        OrderLine = {"quantity":i,"description":"Order Line " + str(i),"unit_price": 12*i,"total": i*i*12}
        OrderLines.append(OrderLine)
        #print(number)

    data = [[u'Quantity', u'Description', u'Price', u'Total'], ]

    
    for item in OrderLines:
        data.append([
            item['quantity'],
            item['description'],
            item['unit_price'],
            item['total']
        ])
    #data.append([u'', u'', u'Total:','544' , '£')],)
    data.append([u'', u'', u'Total:', '£544'])

    ## Items
    #data = [[u'Quantity', u'Description', u'Amount', u'Total'], ]

    
    #for item in invoice.items.all():
    #    data.append([
    #        item.quantity,
    #        item.description,
    #        format_currency(item.unit_price, 'GBP'),
    #        format_currency(item.total(), 'GBP')
    #    ])
    #data.append([u'', u'', u'Total:', format_currency(invoice.total(), invoice.currency)])
    
    table = Table(data, colWidths=[2 * cm, 11 * cm, 3 * cm, 3 * cm])
    #,splitByRow=1,repeatRows=1
    table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
        ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ])
    tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
    table.drawOn(canvas, 1 * cm, -8 * cm - th)

    canvas.showPage()
    canvas.save()
