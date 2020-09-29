# Evidence With Ease
*A nifty Python tool to expedite evidence printing*

This script is aimed at helping debaters who use Google Docs to write their cases and scatter links to evidence all throughout their documents. I know (from personal experience) that it's a nightmare to go through cases two days before a tournament, click on every link, and print each webpage and PDF individually. Even if you have a master evidence sheet or an organized link list, it still takes hours to click and print--hours which could be better spent preparing blocks and fine-tuning arguments. 

## The Program (in a nutshell)
Evidence with Ease utilizes the Python [Requests](https://requests.readthedocs.io/en/master/) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) modules to first scrape your Google Doc for any hyperlinks, then to scrape each linked webpage and download its HTML source code. Next, each HTML file is converted to a PDF using [pdfkit](https://pypi.org/project/pdfkit/). Finally, using PyPDF2's [FileMerger](https://pythonhosted.org/PyPDF2/PdfFileMerger.html), all the PDFs are merged into one big PDF for maximum printing ease. Individual PDFs longer than 30 pages aren't included in the final product (but are still downloaded for you), and should an error occur in either grabbing a webpage's source code or converting it to a PDF, the program will let you know so you can download/print those files afterwards.  

## Clean Printing
You may be familiar with Chrome extensions such as CleanPrint which allow you to remove unnecessary images, headers, styling etc. from webpages to save ink and paper when printing. I created some functions with BeautifulSoup that remove ~80-90% of unwanted tags from the HTML as well as all Javascript and CSS styling before writing to file. It's not a perfect algorithm, and some pages are cleaner than others, but it does the job, and I daresay it does it adequately well.

## Known Issues
Removing Javascript from webpages breaks certain well-devloped sites which generate all page content dynamically, so some 'cleaned' files might not contain any article content at all. Furthermore, removing Javascript looks fishy to sites with good bot detection, so some pages may be blocked or Captcha-prompted. I haven't yet figured out a good way to identify when blocks happen and stop the program from downloading these blocked/Captcha'd pages, but by supplying a realistic user agent and other legitimate browser markers in the request header, I've managed to get around most blocks. In short, don't treat this program as the be-all end-all, and review the final PDF closely for any broken or blocked pages as you'll have to reprint these from the original sources yourself.

*Happy printing!*
*-Sage*
