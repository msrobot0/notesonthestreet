

import lxml
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import green
import shutil,zipfile
from io import BytesIO

#from PyPDF2 import PdfFileWriter,PdfFileReader,PdfFileMerger
from PyPDF3 import PdfFileWriter, PdfFileReader,PdfFileMerger
from PyPDF3.pdf import PageObject
from reportlab.pdfbase.pdfmetrics import stringWidth

import random,os,sys

#mode is img data css css
class Epub:
    def __init__(self,path):
        self.path = path
        self.new_path = None
        self.new_filename= None
        self.root = ""

    #this is sort of crap code
    def get_data(self):
        self.get_epub_data()
        im, css,data = self.get_decorations()
        return im,css, data

    def get_epub_data(self):
        f=open(self.path+"META-INF/"+"container.xml", "r")
        data=f.read()
        soup = BeautifulSoup(data, 'html.parser')
        rootfile=soup.find_all("rootfile")
        try:

            rootfile = rootfile[0]
            fullpath=rootfile.get("full-path")

            if "/" in fullpath:
                first,second = fullpath.split("/")[:2]
                self.new_path= self.path+first+"/"
                self.new_filename = self.new_path+second
                self.root = self.new_filename.split(".")[-1]
            else:
                self.new_path = fullpath
                self.root = self.new_path.split(".")[-1]

            self.root = self.root+":"
        except Exception as er:

            raise Exception("data path error")

    def get_decorations(self):
        f=open(self.new_filename,"r")
        soup = BeautifulSoup(f.read(), 'lxml')

        a=soup.find(self.root+"manifest")
        if a is None:
            self.root = ""
            a=soup.find(self.root+"manifest")
        img = None
        data =None

        try:
            pages=a.find_all(self.root+"item",{"media-type":"application/xhtml+xml"})
            data = pages[random.randint(0,len(pages)-1)].get("href")
            f=open(os.path.join(self.new_path,data),"r")
            data = f.read()
            
        except:
            pass

        try:
            img_jpg=a.find(self.root+"item",{"media-type":"image/jpeg"}).get("href")
            img = os.path.join(self.new_path,img_jpg.split("/")[0]+"/")
        except:
            pass
        try:
            img_png=a.find(self.root+"item",{"media-type":"image/png"}).get("href")
            img =  os.path.join(self.new_path,img_png.split("/")[0]+"/")
        except:
            pass

        
        css_file = None
        try:
            css_file=a.find(self.root+"item",{"media-type":"text/css"}).get("href")
            if css_file is not None:
                css_file  = [os.path.join(self.new_path,css_file)]
        except:
            pass

        return img, css_file, data



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
    pdf_tmp = "/tmp/pdf_tmp/"
    try:
                shutil.rmtree(pdf_tmp)
    except:
        pass

    os.mkdir(pdf_tmp)

    for fn in files:
        pdf_file = None
        in_pdf_file = os.path.join(path,fn)
        if fn[-4:] == "mobi":
            #tempdir, filepath = mobi.extract(in_pdf_file)
            #image_base=filepath[:-9]
            #html=HTML(filename=filepath,base_url=image_base,encoding="utf8")
            #pdf_filename=unzip_file_path.split("/")[-1]
            #pdf_file = fn.replace(".mobi",".pdf")
            #in_pdf_file = pdf_tmp+pdf_file
            #html.write_pdf(in_pdf_file)
            #shutil.rmtree(tempdir)
            pass

        elif fn[-4:] == "epub":
            try:
                tmp_file = "/tmp/epub_temp.zip"
                shutil.copy(in_pdf_file,tmp_file)
                tmp_path="/tmp/epub_temp/"
                try:
                    shutil.rmtree(tmp_path)
                except:
                    pass

                os.mkdir(tmp_path)
                with zipfile.ZipFile(tmp_file, 'r') as zip_ref:
                    ret=zip_ref.extractall(tmp_path)

                pdf_file = fn.replace(".epub",".pdf")
                in_pdf_file = pdf_tmp+pdf_file
                epub = Epub(tmp_path)
                img,css,data = epub.get_data()
                html=HTML(string=data,base_url=img,encoding="utf8")
                html.write_pdf(in_pdf_file,stylesheets=css,font_config=FontConfiguration())

                shutil.rmtree(tmp_path)
            except Exception as e:
                print(e)
                print("err %s" %fn)
        if fn[-3:] == "pdf" or pdf_file is not None:
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
