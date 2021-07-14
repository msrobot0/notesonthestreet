from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import green
import shutil
from io import BytesIO

#from PyPDF2 import PdfFileWriter,PdfFileReader,PdfFileMerger
from PyPDF3 import PdfFileWriter, PdfFileReader,PdfFileMerger
from PyPDF3.pdf import PageObject
from reportlab.pdfbase.pdfmetrics import stringWidth

import random,os,sys

def main():
    args = len(sys.argv)
    total =None
    path = ""
    new_path = ""
    try: 
        if sys.argv[1] == "d":

            new_path = sys.argv[2]    
            shutil.rmtree(new_path)
            os.makedirs(new_path)
            return 
        else:    
            path = sys.argv[1]
            print(path)
            new_path = sys.argv[2]
            try:
              total = int(argv[3])
            except:
              pass
    except: 
    	print("Format is: python main.py source_dir dest_dir optional_max_pdfs")
    files = os.listdir(path)
    
    counter = 0
    for fn in files:
        if fn[-3:] == "pdf":
          try:
             counter += 1
             if total is not None and  counter > total:
               return
             output = PdfFileWriter()
             in_pdf_file = os.path.join(path,fn)
             print(in_pdf_file)
             pdf_file = PdfFileReader(open(in_pdf_file,"rb"))
             num_pages = pdf_file.getNumPages()
             
             i = 0
             if num_pages > 5:
                 i = 3
             i = random.randrange(i,num_pages)
             packet = BytesIO()
             cv=canvas.Canvas(packet,pagesize=letter)
             
             
             title = fn[:-3]+" page:" +str(i)
             
             cv.setLineWidth(5)
             PAGE_HEIGHT = cv._pagesize[1]
             cv.setStrokeColor(green)
             cv.setFillColor(green)
             pdf_text_object = cv.beginText(10,PAGE_HEIGHT-10) 
             pdf_text_object.textOut(title)
             
             cv.drawText(pdf_text_object)
             cv.save()
             packet.seek(0)
             tmp = PdfFileReader(packet)
             template_page= tmp.getPage(0)
             page = pdf_file.getPage(i)
             page.cropBox.upperLeft = (10,500)
             page.cropBox.lowerRight = (1200,1000)

             total_width = max(page.mediaBox.upperRight[0],template_page.mediaBox.upperRight[0])
             total_height = max([page.mediaBox.upperRight[1], template_page.mediaBox.upperRight[1]])

             w = page.mediaBox.upperRight[0] - template_page.mediaBox.upperRight[0]
             h = page.mediaBox.upperRight[1] - template_page.mediaBox.upperRight[1]
             new_page = PageObject.createBlankPage(None, total_width, page.mediaBox.upperRight[1])
             new_page.mergePage(page)
             new_page.mergeTranslatedPage(template_page,w,h)
             
             
             #new_pdf = PdfFileWriter()
             #new_pdf.addPage(outpage)
             output.addPage(new_page)
             out_pdf_file = os.path.join(new_path,"new"+"_"+fn[:-3]+str(i)+".jpg")
             outputStream = open("out.pdf",'wb')
             #output.write(outputStream)
             output.write(outputStream)
             outputStream.close()
		      
             images = convert_from_path('out.pdf')
             images[0].save(out_pdf_file,"JPEG")
              
          except Exception as e:
             print("error: "+str(e))
                 

if __name__ == '__main__':
    main()
