# ReportLab PDF Generation Library
from reportlab.pdfgen        import canvas
from reportlab.lib.units     import inch, cm, mm
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib           import colors

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Spacer, SimpleDocTemplate
from reportlab.platypus.tables import Table, TableStyle

# Constants
Font_Leading = 10
Word_Spacing = 0.0
Char_Spacing = 0.08

#global table
#data= [['DATE', 'NAME', 'ITEM', 'AMOUNT', 'BALANCE'],
#    ['01/12/15', 'William', 'ITEM1 RELATED STUFF', '365.00', '43.30']
#    # CONSIDER MANY MORE ITEMS HERE
#    # NUMBER FO ITMES VARYING IN WAY TO CAUSE 1 OR MORE PAGES
#    # 3RD COLUMN WILL HAVE DESCRIPTIVE ITEM
#    # WHICH WILL REPLACE WITH PARAGARPHS LATER ON
#  ]
data = [[u'Quantity', u'Description', u'Price', u'Total', u'*'], ]
#Test Lines
Order = {}
Order["OrderLines"] = []
OrderLines = Order["OrderLines"]

#make 30 lines
for i in range(1,101):
    OrderLine = {"quantity":i,"description":"Order Line " + str(i),"unit_price": 12*i,"total": i*i*12,"*": 0}
    OrderLines.append(OrderLine)
    #print(number)

#make 30 lines
for item in OrderLines:
    data.append([
        item['quantity'],
        item['description'],
        item['unit_price'],
        item['total'],
        item['*']
    ])

data.append([u'', u'', u'Total:', '£544',u''])

t=Table(data,repeatRows=1,
  colWidths=[.7*inch, 1*inch, 2.4*inch, .8*inch, .8*inch])
 #The top left cell is (0, 0) the bottom right is (-1, -1).
tStyle = TableStyle([
    # All Cells
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEADING', (0,0), (-1,-1), 10),
    # Top row
    ('BACKGROUND', (0,0), (-1,0), colors.maroon),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('ALIGN', (0,0), (-1,0), 'CENTRE'),
    # 3RD and 4th column,
    ('ALIGN', (3,0), (4,-1), 'RIGHT'),
    # Line commands
    # All
    ('BOX',(0,0),(-1,-1),.5,colors.black),
    # top row
    ('GRID',(0,0),(-1,0),.5,colors.black),
    # all columns
    ('LINEBEFORE',(0,0),(-1,-1),.5,colors.black),
    # last column
    ('LINEAFTER',(-1,0),(-1,-1),.5,colors.black),
    # last row
    ('LINEBELOW',(0,-1),(-1,-1),.5,colors.black)])
t.setStyle(tStyle)




def othPg(c, doc):
  t.colWidths = [.2*inch, .2*inch,4*inch, .2*inch, .2*inch]
  tStyle.add('BACKGROUND',(0,0),(-1,-1),colors.lightblue)
  x=1

def pgHdr(c, doc):
  width,height = A4
  c.saveState()
  c.translate(.3 * inch, 0 * inch)

# STUFF RELATED TO 2 INCH STTIC HEADER FOR FIRST PAGE
  c.restoreState()

def main_simple(sFilename):
  pdf_file = sFilename
  Elements = []
  doc = SimpleDocTemplate(pdf_file,
                        pagesize=A4,
                        leftMargin=.3*inch,
                        rightMargin= .1 * inch,
                        topMargin= .1 * inch,
                        bottomMargin=.3 * inch,
                        showBoundary=1)

  
  styles=getSampleStyleSheet()
  ptext = '<font size=12><b>Sample Report Heading</b></font>'

  Elements.append(Paragraph(ptext, styles["Normal"]))
  Elements.append(Spacer(1, 12))
  Elements.append(t)

  doc.build(Elements, canvasmaker=PageNumCanvas)



def main(sFilename):
  pdf_file = sFilename
  Elements = []
  doc = BaseDocTemplate(pdf_file,
                        pagesize=A4,
                        leftMargin=.3*inch,
                        rightMargin= .1 * inch,
                        topMargin= .1 * inch,
                        bottomMargin=.3 * inch,
                        showBoundary=1)
  #normal frame as for SimpleFlowDocument
  #frameT = Frame(doc.leftMargin + 2*inch, doc.bottomMargin, doc.width - 2.01*inch, doc.height - 4.1*inch, id='normal', showBoundary=0)
  #frameB = Frame(doc.leftMargin+2, doc.bottomMargin, 7.5*inch, 10*inch, id='small', showBoundary=1)

  frameT = Frame(doc.leftMargin , doc.bottomMargin, doc.width - 0.5*inch, doc.height - 1*inch, id='normal', showBoundary=0)
  frameB = Frame(doc.leftMargin , doc.bottomMargin, doc.width - 0.5*inch, doc.height - 1*inch, id='normal', showBoundary=1)
  



  doc.addPageTemplates([PageTemplate(id='First',frames=frameT,onPage=pgHdr),
                        PageTemplate(id='Later',frames=frameB,onPage=othPg)
                      ])
  Elements.append(NextPageTemplate('Later'))
  Elements.append(t)

  #doc.addPageTemplates([PageTemplate(id='First',onPage=pgHdr)])
  #Elements.append(BaseDocTemplate)
  #Elements.append(t)

  doc.build(Elements)

  doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
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
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        #self.drawRightString(195*mm, 272*mm, page)
        self.drawRightString(195*mm, 10*mm, page)


if __name__ == "__main__":
    sys.exit(main())
