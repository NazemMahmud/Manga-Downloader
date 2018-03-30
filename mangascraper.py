# Manga scraping and downloading 

# Requirements: 
#   - Python 3.x 
#   - BeautifulSoup4
#   - PIP
#   - Requests

# Goals
#   -  Scrape MangaDex or MangaFox for web page information.
#   -  Download image files of manga. (Requests and Shutil)
#   -  Convert manga names appropriately
#   -  Setup query correctly to retrieve correct files from name.
#   -  Convert images to pdf or appropriate extension for viewing on KindleFire
#   -  Create simple front end GUI
#   -  Wrap project up for 'release'



from bs4 import BeautifulSoup as bs  # Source code parsing
import re  # Regular expressions
import sys
import requests # HTTP Requests
import shutil #Advanced file handling
import os # Directory operations
from sys import platform # check platform
from fpdf import FPDF
import glob


#Constants
PROVIDER = "https://www.mangareader.net/"
INITIAL_PAGE = 1
SUCCESS_MSG = "\tDownloaded successfully!"
DOWNLOAD_MSG = "\tDownloaded page #"
NOTFOUND_MSG = "Queried Manga not found."
REQUEST_ERR = "Requested page could not be reached." 
FILE_EXT = ".jpg" 



def sendRequest(url, binary = False):
  try:
    request = requests.get(url, stream = binary)
  except:
    print(REQUEST_ERR)
    exit()
  return request


def downloadImage(url, downloadPath, page):
  if not os.path.exists(downloadPath):
    os.makedirs(downloadPath)

  imgName = addZeroes(str(page), 3) + FILE_EXT
  imgPath = downloadPath + imgName
  request = sendRequest(url, True)
  
  with open(imgPath, 'wb') as filePath:
    request.raw.decode_content = True
    shutil.copyfileobj(request.raw, filePath)

  print(DOWNLOAD_MSG + str(page))




def getDownloadPath(series, chapter, path):
  return path + series.title() + "/Chapter-" + addZeroes(str(chapter), 4)  + "/"

def getPageURL(series, chapter, page = 1):
  return PROVIDER + dashes(series) + "/" + str(chapter) + "/" + str(page)

def dashes(series):
  return re.sub("\s+", "-", series.lower())

def addZeroes(num, maxDigits):
  digits = len(num)
  zeroes = "0" * (maxDigits - digits)
  return zeroes + num 

def yesOrNo(question):
  reply = str(input(question + ' (y/n): ')).lower().strip()
  if reply[0] == 'y':
    return True
  if reply[0] == 'n':
    return False
  else:
    return yesOrNo("Invalid Input. Try Again.")

def clearScreen():
  if platform == "win32":
    os.system('cls')
  elif platform == "linux":
    os.system('clear')
  


def downloadMangaChapter(seriesName, chapter, path):
  downloadPath = getDownloadPath(seriesName, chapter, path)
  currentPage = INITIAL_PAGE
  print ("  Retrieving", seriesName, "Chapter", chapter, "and saving to\n    " + downloadPath)

  # Loop through all pages of chapter until there are none left
  while True:
    pageURL = getPageURL(seriesName, chapter, currentPage)
    request = sendRequest(pageURL)
    rawHTML = request.text

    if request.status_code != 200 or not len(rawHTML):
      print (NOTFOUND_MSG if not len(rawHTML) else SUCCESS_MSG)
      break

    # Scrape the HTML
    parsedHTML = bs(rawHTML, "html.parser")
    imgURL = parsedHTML.find("img", {"id" : "img"}).get("src")  

    downloadImage(imgURL, downloadPath, currentPage)
    currentPage = currentPage + 1


def createPDF(seriesName, chapter, path):
  downloadPath = getDownloadPath(seriesName, chapter, path)
  imageList = glob.glob(downloadPath + "/*.jpg")
  
  

  pdf = FPDF('P', 'mm', (281.7, 413))
  #pdf = FPDF('P', 'mm')
  pdf.set_auto_page_break(False, 0.0)
  pdf.set_margins(0.0, 0.0, 0.0)
  pdf.set_display_mode('fullpage', 'single')

  for image in sorted(imageList): 
    pdf.add_page()
    pdf.image(image)
  
  print("  Finished building PDF for", seriesName,"-Chapter", chapter, "with", len(imageList), "pages")
  pdf.output(downloadPath + "/" + seriesName + "-" + addZeroes(str(chapter), 4), "F")



def main(): 
  path = os.getcwd() + "/Manga/" 

  while True:
    clearScreen()
    print("----------- Manga Downloader V1 -------------")
    print("\n  NOTE: Manga is currently only downloaded from mangareader.net") 
    title = input("\n\tEnter Series Name: ").title()
    chapterStart = int(input("\tEnter Chapter Range Start : "))
    chapterEnd = int(input("\tEnter Chapter Range End : ")) 

    print ("\tDownloading Chapters", chapterStart, "-", chapterEnd, "\n")

    for chapter in range(chapterStart, chapterEnd+1):
      downloadMangaChapter(title, chapter, path) 
      print("  Finished Downloading",title, "Chapter", chapter)
      createPDF(title, chapter, path)

    print("\n  Finished download request")
    
    if not yesOrNo("  Download more? "):
      break 

# Run main program loop
main()



