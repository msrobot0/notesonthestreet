
   
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration
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


#mode is img data css css
def get_epub_data(path,filename):

    f=open(path+"META-INF/"+"container.xml", "r")
    data=f.read()
    soup = BeautifulSoup(data, 'html.parser')
    rootfile=soup.find_all("rootfile")
    try:
        rootfile = rootfile[0]
        fullpath=rootfile.get("full-path")
        if "/" in fullpath:
            first,second = fullpath.split("/")[:2]      
            
            new_path= path+first+"/"
            f=open(new_path+second,"r")
            soup = BeautifulSoup(f.read(), 'lxml')
            a=soup.find("manifest")
            ncx_file=a.find(id="ncx").get("href")
            f.close()
            if(ncx_file is None):
                print ("err 41")
                return None
                
            f=open(os.path.join(new_path,ncx_file),"r")
            return f.read()
        else:
            
            f=open(os.path.join(path,fullpath),"r")
            soup = BeautifulSoup(f.read(), 'lxml')
            a=soup.find("manifest")
            ncx_file=a.find(id="ncx").get("href")
            f.close()
            if(ncx_file is None):
                print("NCX file not found 55")
                
            f.close()
            f=open(os.path.join(path,ncx_file),"r")
            return f.read()
    except:
        print ("err 61")
        return None

def get_epub(mode="img",path,filename):
    f=open(path+filename,"r")
    soup = BeautifulSoup(f.read(), 'lxml')
    a=soup.find("manifest")
    if mode == "img":
        try:
            img_jpg=a.find("item",{"media-type":"image/jpeg"}).get("href")
            return path+img_jpg.split("/")[0]+"/"
        except:
            pass
        try:
            img_png=a.find("item",{"media-type":"image/png"}).get("href")
            return global_root_dir+img_png.split("/")[0]+"/"
        except:
            return None


    if mode == "css":
        css_file=a.find("item",{"media-type":"text/css"}).get("href")
        if css_file is None: 
            return None
        else: 
            return [os.path.join(path,css_file)]
        

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
    	pdf_file = None
    	in_pdf_file = os.path.join(path,fn)
    	if fn[-4:] == "mobi":
			tempdir, filepath = mobi.extract(in_pdf_file)
			image_base=filepath[:-9]
			html=HTML(filename=filepath,base_url=image_base,encoding="utf8")
			pdf_filename=unzip_file_path.split("/")[-1]
    		pdf_file = fn.replace(".mobi",".pdf")
            html.write_pdf(new_filename)
    		shutil.rmtree(tempdir)
    	elif fn[-4:] == "epub":
             
              html=HTML(string=get_epub_data(path,fn),base_url=get_epub("img",path,fn),encoding="utf8")
              pdf_file = fn.replace(".epub",".pdf")
              html.write_pdf(pdf_file stylesheets=get_epub("css",path,fn),font_config=FontConfiguration())
              print "ok"
        if False #fn[-3:] == "pdf" or pdf_file is not None:
          try:
             counter += 1
             if total is not None and  counter > total:
               return
             output = PdfFileWriter()
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
