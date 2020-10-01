#!/usr/bin/python3
import re, os
from tkinter import *
from tkinter import filedialog

import pdfkit, requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

# important global variables:
downloadFolder = False
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "Referer": 'https://google.com',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
def initVars():
    global file_paths
    file_paths = []
    global failed_files
    failed_files = []
    global pdfs_for_merge
    pdfs_for_merge = []
    global merger
    merger = PdfFileMerger(strict=False)


# Functions to retrieve the GDoc and scrape links:
def getUrl():
    url = urlEntry.get()
    return url

def getTitleAndLinks(url):
    res = requests.get(url, headers=headers)
    print(res.status_code)
    g_doc_soup = BeautifulSoup(res.text, 'lxml')
    doc_title = g_doc_soup.find('span', {"id":"docs-title-input-label-inner"})
    doc_title = str(doc_title.text)
    urls = re.findall(r'(?<=ulnk_url":")(\S+?)(?="}})', res.text)
    return [urls, doc_title]

# Functions to be called on each 
# iteration through links list:
def removeTags(tag):
    [assessImportance(parent) for parent in tag.parents]
    if tag and not tag.find(['ul', 'ol']):
        tag.decompose() 
        
def assessImportance(tag):
    if not tag.find(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tag.decompose()

def removeStyle(tag):
    if 'style' in tag.attrs:
        del tag.attrs['style']

def writeFile(soup, url, title):
    try: 
        output = '%s/%s.html' % (downloadFolder, title)
        open(output, 'w', encoding='utf-8-sig').write(str(soup))
        file_paths.append(output)
    except: 
        failed_files.append('CRAPCAKES! Could not save webpage: %s (%s). Go to website and print directly!' % (title, url))

# Iterate through links list--retrive, clean, 
# and download HTML of each linked page:
def scrapeUrls(urls):
    for index, url in enumerate(urls):
        print('%s/%s %s' %(index + 1, len(urls), url))
        try: 
            res = requests.get(url, headers=headers)
            content_type = res.headers.get('content-type')
            if 'application/pdf' in content_type: #just download it
                output = '%s/pdf%s.pdf' % (downloadFolder, index + 1)
                open(output, 'wb').write(res.content)
                file_paths.append(output)
            else: #clean page HTML and write to temporary local file
                soup = BeautifulSoup(res.text, 'lxml')
                number = str(index + 1)
                title = '%s) %s' % (number, soup.title.text.strip()) if soup.title is not None else number
    
                [script.decompose() for script in soup.find_all('script')]
                unwanted_tags = soup.find_all(['nav', 'img', 'iframe', 'embed', 'picture', 'video', 'form', 'input', 'textarea', 'canvas', 'ul', 'ol', 'svg', 'link', 'header', 'style', 'footer'])
                [removeStyle(tag) for tag in soup.find_all()]
                [removeTags(tag) for tag in unwanted_tags]

                writeFile(soup, url, title)
        except:
            failed_files.append('GOSHDARN! Could not download webpage %s. Visit URL and try to print from browser.' % url)


# Functions for making PDFs
# from HTML files:
def makePDF(index, file):
    try: 
        out = '%s/html%s.pdf' % (downloadFolder, index + 1)
        print('Job %s (%s): ' %(index + 1, file))
        head = file.replace('%s/' % downloadFolder, '')
        pdfkitOptions = {
            'page-size': 'Letter',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            "header-left": head,
            "header-right":"[page]/[toPage]",
            "header-line":"",
            "header-font-size":10
        } 
        pdfkit.from_file(file, out, options=pdfkitOptions)
        pdfs_for_merge.append(out)
        os.remove(file)
    except:
        fail = 'SHUCKS! Could not make PDF of %s; not included in final product. Open the file and print directly!\n' % file
        failed_files.append(fail)

def makePDFlist(file_paths):
    for index, file in enumerate(file_paths):
        if not re.search(r'pdf$', file):
            makePDF(index, file)  
        else:
            doc = open(file, 'rb')
            reader = PdfFileReader(doc)
            numPages = reader.getNumPages()
            if numPages < 30:
                pdfs_for_merge.append(file)
            else: #don't waste paper
                failed_files.append("WOWZERS! %s is over 30 pages long--don't bother printing it out! The file has already been saved for you in the target folder." % file)


# Functions for adding blanks 
# and merging all PDFs:
def addPage(pdf, reader, merger): 
    outPdf = PdfFileWriter()
    outPdf.appendPagesFromReader(reader)
    outPdf.addBlankPage()
    temp = '%s/temp.pdf' % downloadFolder
    output = open(temp, 'wb')
    outPdf.write(output)
    output.close() 
    merger.append(temp, import_bookmarks=False)
    os.remove(temp)
    print('\nBlank page added to %s to avoid double-sided printing issues!' % pdf)
    
def mergePDFs(pdfs):
    for pdf in pdfs:
        file = open(pdf, 'rb')
        reader = PdfFileReader(file)
        numPages = reader.getNumPages()
        # add a blank page to docs with an 
        # odd number of pages to save headache...
        if not (numPages % 2) == 0:
            addPage(pdf, reader, merger)  
        else: 
            merger.append(pdf, import_bookmarks=False)
        os.remove(pdf)


# THE MASTER "GO!" FUNCTION:
def runFuncs():
    if not downloadFolder == False: 
        initVars()
        url = getUrl()
        titleAndLinks = getTitleAndLinks(url)
        urls = titleAndLinks[0]
        doc_title = titleAndLinks[1]
        scrapeUrls(urls)
        makePDFlist(file_paths)
        mergePDFs(pdfs_for_merge)
        merger.write('%s/EVIDENCE %s.pdf' % (downloadFolder, doc_title))
        print('\n\nJob complete! Find your clean, print-friendly PDF at %s/EVIDENCE %s.pdf\nRemarks:' % (downloadFolder, doc_title))
        [print(fail) for fail in failed_files]
    else:
        print('YIKES! Choose a download folder!')


# Simple Tkinter GUI:
root = Tk()

urlEntry = Entry(root, width=50)
urlEntry.grid(row=0, column=0)

goButton = Button(root, width=10, text="Go!", command=runFuncs)
goButton.grid(row=0, column=1)

def getDownloadFolder():
    global downloadFolder
    downloadFolder = filedialog.askdirectory()
    print('Target folder: %s' % downloadFolder)

folder_select = Button(root, width=60, text="Choose download folder", command=getDownloadFolder)
folder_select.grid(row=1, columnspan=2)
# Script entry point 
def main():
    root.mainloop()