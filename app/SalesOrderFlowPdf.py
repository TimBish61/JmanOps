# ReportLab PDF Generation Library
from reportlab.pdfgen        import canvas
from reportlab.lib.units     import inch, cm, mm
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib           import colors

from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

from app.models import SoHeader, SoDetail2, Currency, SYSTEM_MAIN, SYSTEM_BANK
from django.db.models import Sum
import datetime
from JmanOps.InvoiceSettings import settings, INV_LOGO

# Constants
Font_Leading = 10
Word_Spacing = 0.0
Char_Spacing = 0.08

myOrderId=None

def get_table(invoice):

    #global table
    oOrderLines=SoDetail2.objects.filter(soheader=invoice.id).order_by('SOLineNumber')
    OrderLineCount=oOrderLines.count()
    SumOrderNet=oOrderLines.aggregate(Sum('SONet'))
    SumOrderNet=SumOrderNet['SONet__sum']
    SumOrderVat=oOrderLines.aggregate(Sum('SOVat'))
    SumOrderVat=SumOrderVat['SOVat__sum']
    SumOrderGross=SumOrderNet+SumOrderVat

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_LEFT

    data = [[u'Description', u'Quantity', u'Price '+invoice.SOCurrency.Symbol, u'Total '+invoice.SOCurrency.Symbol], ] 

    
    #.replace('\r\n','<br />\n')
    for i in range(1,OrderLineCount+1):             
        description = Paragraph('#'+str(oOrderLines[i-1].SOLineNumber)+' '+oOrderLines[i-1].SODetail.replace('\r\n','<br />\n'), styleN)
        data.append([
            description,
            "{:.1f}".format(oOrderLines[i-1].SOQty),
            "{:,.2f}".format(oOrderLines[i-1].SOSalesPrice),
            "{:,.2f}".format(oOrderLines[i-1].SONet)
        ])



    t=Table(data,repeatRows=1,
      colWidths=[11 * cm, 2 * cm, 3 * cm, 3 * cm])
     #The top left cell is (0, 0) the bottom right is (-1, -1).
    tStyle = TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                ('GRID', (0, 0), (-1, -1), 1, (0.7, 0.7, 0.7)),
                ('ALIGN', (-3, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),])
    t.setStyle(tStyle)

    return t

def get_summary_table(invoice):

    #global table
    oOrderLines=SoDetail2.objects.filter(soheader=invoice.id).order_by('SOLineNumber')

    SumOrderNet=oOrderLines.aggregate(Sum('SONet'))
    SumOrderNet=SumOrderNet['SONet__sum']
    SumOrderVat=oOrderLines.aggregate(Sum('SOVat'))
    SumOrderVat=SumOrderVat['SOVat__sum']
    SumOrderGross=SumOrderNet+SumOrderVat

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

    return tableTotal

def main_simple(sFilename,invoice):
  pdf_file = sFilename
  t = get_table(invoice)
  Elements = []
  doc = SimpleDocTemplate(pdf_file,
                        pagesize=A4,
                        leftMargin=.3*inch,
                        rightMargin= .1 * inch,
                        topMargin= 1 * inch,
                        bottomMargin=1 * inch,
                        showBoundary=0)

  
  styles=getSampleStyleSheet()
  ptext = '<font size=14><b>Sample Report Heading</b></font>'

  Elements.append(Paragraph(ptext, styles["Normal"]))

  Elements.append(Spacer(1, 30))

  Elements.append(t)

  doc.build(Elements, canvasmaker=PageNumCanvas)
    
def main(sFilename,invoice):
    pdf_file = sFilename
    t = get_table(invoice)
    Elements = []

    def pgHdr(c, doc):
      width,height = A4
      #c.saveState()
      #c.translate(.3 * inch, 0 * inch)

      # STUFF RELATED TO 2 INCH STTIC HEADER FOR FIRST PAGE
      #c.restoreState()
    def othPg(c,doc):
      width,height = A4


    styles = getSampleStyleSheet()
    Elements.append(Spacer(1,2*inch))
    style = styles["Normal"]

    for i in range(3):
        bogustext = ("This is Paragraph number %s.  " % i) * 2
        p = Paragraph(bogustext, style)
        Elements.append(p)
        Elements.append(Spacer(1,0.2*inch))

    doc = BaseDocTemplate(pdf_file,
                    pagesize=A4,
                    leftMargin=.3*inch,
                    rightMargin= .1 * inch,
                    topMargin= .1 * inch,
                    bottomMargin=.3 * inch,
                    showBoundary=0)
    #normal frame as for SimpleFlowDocument
    #frameT = Frame(doc.leftMargin + 2*inch, doc.bottomMargin, doc.width - 2.01*inch, doc.height - 4.1*inch, id='normal', showBoundary=0)
    #frameB = Frame(doc.leftMargin+2, doc.bottomMargin, 7.5*inch, 10*inch, id='small', showBoundary=0)

    frameT = Frame(doc.leftMargin , doc.bottomMargin + 1*inch, doc.width, doc.height, id='normal', showBoundary=0)
    frameB = Frame(doc.leftMargin , doc.bottomMargin + 1*inch, doc.width, doc.height, id='normal', showBoundary=0)

  



    doc.addPageTemplates([PageTemplate(id='First',frames=frameT,onPage=pgHdr),
                        PageTemplate(id='Later',frames=frameB,onPage=othPg)
                        ])
    Elements.append(NextPageTemplate('First'))
    Elements.append(NextPageTemplate('Later'))
    Elements.append(t)

    #doc.addPageTemplates([PageTemplate(id='First',onPage=pgHdr)])
    #Elements.append(BaseDocTemplate)
    #Elements.append(t)

    doc.build(Elements)

def main_header(sFilename,invoice):

    myOrderId=invoice.pk
    canvas.setTitle=invoice.pk
        
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    styleB = styles['BodyText']


    

    Elements=[]
    t = get_table(invoice)

    def coord(obj, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, y  * unit - obj.height
        return x, y

    def draw_main_doc_header(canvas, pdf):
        """ Draws the invoice header """
        canvas.saveState()
        canvas.translate(0, 29.7 * cm)
        canvas.setFont('Helvetica', 10)
        canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
        canvas.setFillColorRGB(0.2, 0.2, 0.2)
        canvas.setFont('Helvetica', 16)
        canvas.drawString(18 * cm, -1 * cm, 'Invoice')
        canvas.drawInlineImage(INV_LOGO, 1 * cm, -1 * cm, 25, 25)
        canvas.setLineWidth(4)
        canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)
        canvas.restoreState()

    def draw_sys_address(canvas, pdf):
        """ Draws the business address """
        #canvas.saveState()
        #canvas.translate(0, 29.7 * cm)
        oCompany=get_object_or_404(SYSTEM_MAIN, pk=1)
        business_details = (
            u''+ oCompany.CompanyName +'',
            u''+ oCompany.Address +'',
            u''+ oCompany.Town +'',
            U''+ oCompany.County +'',
            U''+ oCompany.PostCode +'',
            U''+ oCompany.Country +'',
            u'',
            u'Phone: '+ oCompany.Phone +'',
            u'Email: '+ oCompany.Email +'',
            u'Website: '+ oCompany.Website +'',
            u'VAT No: '+ oCompany.CoVatNo +'',
            u'Reg No:'+ oCompany.CoRegNo +''
        )        

        address='<font size="9">'
        for line in business_details:
            address=address+line+'<br/>'
        address=address+'</font>'

        heading=None
        heading = Paragraph(address, styleB)
        heading.wrap(pdf.width, 2*inch)
        #heading.drawOn(canvas,pdf.leftMargin + 12*cm, -8*cm)
        x, y=coord(heading, pdf.leftMargin/cm + 12 , 27, cm)
        heading.drawOn(canvas,x, y)
        #canvas.restoreState()
    
    def draw_cust_address(canvas, pdf,invoice):
        """ Draws the business address """
        #canvas.saveState()
        #canvas.translate(0, 29.7 * cm)
        address='<font size="9">'
        address=address+invoice.customer.Name+'<br/>'
        addresslines=invoice.customer.Address.split('\r\n')
        for addressline in addresslines:
            address=address+addressline+'<br/>'
        if invoice.customer.Town:
            address=address+invoice.customer.Town+'<br/>'
        if invoice.customer.County:
            address=address+invoice.customer.County+'<br/>'
        address=address+invoice.customer.PostCode+'<br/>'
        address=address+invoice.customer.Country+'<br/>'
        address=address+'</font>'

        heading=None
        heading = Paragraph(address, styleB)
        heading.wrap(pdf.width, 2*inch)
        #heading.drawOn(canvas,pdf.leftMargin, -8*cm)
        x, y=coord(heading, pdf.leftMargin/cm , 27, cm)
        heading.drawOn(canvas,x, y)
        #heading.drawOn(canvas,coord(heading, pdf.leftMargin, -1.5*cm, cm))
        #canvas.restoreState()

    def draw_footer(canvas,pdf):
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

    def header(canvas, pdf):

        draw_cust_address(canvas, pdf,invoice)

        draw_sys_address(canvas, pdf)

        topPosition=24
        
        subheading=contPara(invoice,1)
        subheading.wrap(pdf.width, inch * 1)
        x, y=coord(subheading, pdf.leftMargin/cm , topPosition, cm)
        subheading.drawOn(canvas,x, y)

        subheading=contPara(invoice,2)
        subheading.wrap(pdf.width, inch * 1)
        x, y=coord(subheading, pdf.leftMargin/cm+2 , topPosition, cm)
        subheading.drawOn(canvas,x, y)

    def continuation(canvas, pdf):
        topPosition=26
        
        subheading=contPara(invoice,1)
        subheading.wrap(pdf.width, inch * 1)
        x, y=coord(subheading, pdf.leftMargin/cm , topPosition, cm)
        subheading.drawOn(canvas,x, y)

        subheading=contPara(invoice,2)
        subheading.wrap(pdf.width, inch * 1)
        x, y=coord(subheading, pdf.leftMargin/cm+2 , topPosition, cm)
        subheading.drawOn(canvas,x, y)

    def contPara(invoice,colmn):

        if colmn==1:
            ContinueText='<font size="9">'
            ContinueText=ContinueText+u'Invoice ID:<br/>'
            ContinueText=ContinueText+u'Invoice Date:<br/>'
            ContinueText=ContinueText+u'Client:<br/>'
            ContinueText=ContinueText+'</font>'

            subheading = Paragraph(ContinueText, styleN)
        else:
            ContinueText='<font size="9">'
            ContinueText=ContinueText+u''+str(invoice.SONumber)+'<br/>'
            ContinueText=ContinueText+u''+"{:%d %b %Y}".format(invoice.order_date)+'<br/>'
            ContinueText=ContinueText+u''+invoice.customer.Code+': ' + invoice.customer.Name+'<br/>'
            ContinueText=ContinueText+'</font>'
            subheading = Paragraph(ContinueText, styleN)
        return subheading

    pdf = BaseDocTemplate(sFilename, pagesize=letter)
    frame = Frame(
        pdf.leftMargin,
        pdf.bottomMargin + 1 * inch,
        pdf.width,
        pdf.height - inch * 3,
        showBoundary=0)  # Delete to remove line around the frame.
    frame2 = Frame(
        pdf.leftMargin,
        pdf.bottomMargin + 1.5*inch,
        pdf.width,
        pdf.height - inch * 2,
        showBoundary=0)  # Delete to remove line around the frame.

    template1 = PageTemplate(id='first_page', frames=frame, onPage=header)
    pdf.addPageTemplates([template1])
    template2 = PageTemplate(id='all_pages', frames=frame2, onPage=continuation)
    pdf.addPageTemplates([template2])
    ## Data for table
    #data = [["String", "String", "Number", "Number", "Number"]]
    #data.extend([["one", "two", i, i, i] for i in range(90)])
    ## Styles for table
    #table_style = TableStyle([
    #    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
    #    ('ALIGN', (2, 0), (4, -1), 'RIGHT'),
    #])

    Elements.append(NextPageTemplate('first_page'))
    Elements.append(NextPageTemplate('all_pages'))
    # Create table and repeat row 1 at every split.
    #table = Table(data, repeatRows=1, style=table_style)
    Elements.append(t)

    #Elements.append(Spacer(1,0.75*inch))

    #tblTotal=get_summary_table(invoice)
    #Elements.append(tblTotal)
    
    testid=myOrderId

    canvas.Canvas.docno={'docno': myOrderId, 'docCy': invoice.SOCurrency.Symbol}

    pdf.build(Elements, canvasmaker=DocPageNumCanvas)



class DocPageNumCanvas(canvas.Canvas):
    def __init__(self, docno, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, docno, *args, **kwargs)
        self.pages = []

            #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            if(self._pageNumber==page_count):
               self.draw_doc_totals_footer(page_count)
               self.draw_bank_footer(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------    
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(195*mm, 10*mm, page)
    #----------------------------------------------------------------------
    def draw_doc_totals_footer(self, page_count):

        oOrderLines=SoDetail2.objects.filter(soheader=self.docno['docno']).order_by('SOLineNumber')
        SumOrderNet=oOrderLines.aggregate(Sum('SONet'))
        SumOrderNet=SumOrderNet['SONet__sum']
        SumOrderVat=oOrderLines.aggregate(Sum('SOVat'))
        SumOrderVat=SumOrderVat['SOVat__sum']
        SumOrderGross=SumOrderNet+SumOrderVat
        #docCy
        datatotal=[[u'', u'', u'Net '+self.docno['docCy']+':', u''+str("{:,.2f}".format(SumOrderNet))]]
        datatotal.append([u'', u'', u'VAT '+self.docno['docCy']+':', u''+str("{:,.2f}".format(SumOrderVat))])
        datatotal.append([u'', u'', u'Total '+self.docno['docCy']+':', u''+str("{:,.2f}".format(SumOrderGross))])

        #datatotal=[[u'', u'', u'Net :', u''+str("{:,.2f}".format(SumOrderNet))]]
        #datatotal.append([u'', u'', u'VAT :', u''+str("{:,.2f}".format(SumOrderVat))])
        #datatotal.append([u'', u'', u'Total :', u''+str("{:,.2f}".format(SumOrderGross))])

        #datatotal=[[u'', u'', u'Net :', u''+str("{:,.2f}".format(12))]]
        #datatotal.append([u'', u'', u'VAT :', u''+str("{:,.2f}".format(0))])
        #datatotal.append([u'', u'', u'Total :', u''+str("{:,.2f}".format(12))])

        tableTotal = Table(datatotal, colWidths=[11 * cm, 2 * cm, 3 * cm, 3 * cm])
        tableTotal.setStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
            ('GRID', (2, 0), (3, -1), 1, (0.7, 0.7, 0.7)),
            ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
            ])
        tw, th, = tableTotal.wrapOn(self, 15 * cm, 19 * cm)
        #lmargin=self._doctemplate.leftMargin/2
        tableTotal.drawOn(self, 1 * cm + 9 , 4 * cm)

    def draw_bank_footer(self, page_count):
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
        textobject = self.beginText(1 * cm, 4 * cm)
        for line in note:
            textobject.textLine(line)
        self.drawText(textobject)
        



if __name__ == "__main__":
    sys.exit(main())
