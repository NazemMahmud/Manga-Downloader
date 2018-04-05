# Manga scraping and downloading 

# Requirements: 
#   - Python 3.x 
#   - BeautifulSoup4
#   - PIP
#   - Requests
# Konjiki No Moji Tsukai - Yuusha Yonin Ni Makikomareta Unique Cheat <-- Test for downloading all even if some chapter are missing


from bs4 import BeautifulSoup as bs  # Source code parsing
import re  # Regular expressions
import sys
import requests # HTTP Requests
import shutil #Advanced file handling
import os # Directory operations
from sys import platform # check platform
import glob
import zipfile


#Constants
PROVIDER = "https://www.mangareader.net/"
FILE_EXT = ".jpg" 
PROGRAM_TITLE = "Barrett's Manga Downloader"




def sendRequest(url, binary = False):
  try:
    request = requests.get(url, stream = binary)
  except KeyboardInterrupt:
    endProgram("\n  Keyboard Interruption detected.\n  Download interrupted.\n  CBZ file was not created.")
  except:
    endProgram("\n  Request could not be made.\n  Download Interrupted.\n  CBZ file was not created.")
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



def getDownloadPath(series, chapter, path):
  return path + series.title() + "/Chapter-" + addZeroes(str(chapter), 4)  + "/"

def getPageURL(series, chapter, page = 1):
  return PROVIDER + dashes(series) + "/" + str(chapter) + "/" + str(page)

def getSearchURL(search):
  return PROVIDER + "search/?w=" + spaceToPlus(search)

def dashes(text):
  return re.sub("\s+", "-", text.lower())

def spaceToPlus(text):
  return re.sub("\s+", "+", text.lower())

def addZeroes(num, maxDigits):
  digits = len(num)
  zeroes = "0" * (maxDigits - digits)
  return zeroes + num 

def yesOrNo(question):
  try:
    reply = str(input(question + ' (y/n): ')).lower().strip()
  except KeyboardInterrupt:
      endProgram("\n  Keyboard Interruption detected.")
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

def drawHeader():
  print("-----------", PROGRAM_TITLE, "-------------")
  print("\n  NOTE: Manga is currently only downloaded from mangareader.net")



def downloadMangaChapter(seriesName, chapter, path, endRange):
  downloadPath = getDownloadPath(seriesName, chapter, path)
  currentPage = 1
  print ("\n  Retrieving", seriesName, "Chapter", chapter, "and saving to\n    " + downloadPath)
  totalPages = 0

  # Loop through all pages of chapter until there are none left
  while currentPage:
    pageURL = getPageURL(seriesName, chapter, currentPage)
    request = sendRequest(pageURL)
    rawHTML = request.text

    if request.status_code != 200 or not len(rawHTML):
      break
    parsedHTML = bs(rawHTML, "html.parser")

    # Get total pages
    if currentPage == 1:
      dropdown = parsedHTML.find("select", {"id" : "pageMenu"})
      totalPages = int(len(dropdown) / 2)

    imgURL = parsedHTML.find("img", {"id" : "img"}).get("src")
    try:
      downloadImage(imgURL, downloadPath, currentPage)
    except KeyboardInterrupt:
      endProgram("\n  Keyboard Interruption detected.\n  Download interrupted.\n  CBZ file was not created.")

    print("\tDownloaded Page {} of {}".format(currentPage, totalPages), end = '\r')
    currentPage = currentPage + 1



def createCBZ(seriesName, chapter, path):
  downloadPath = getDownloadPath(seriesName, chapter, path)
  imageList = glob.glob(downloadPath + "/*" + FILE_EXT)
  try:
    zip = zipfile.ZipFile(downloadPath +  seriesName + "-" + addZeroes(str(chapter), 4) + ".cbz", mode='w')
  except:
    print("\n  Unable to find", seriesName, " Chapter", chapter, ". Unable to create a .CBZ file for it.")
    return
  try:
    for i, image in enumerate(sorted(imageList)):
      zip.write(image)
  finally:
    print("  Created CBZ File for", seriesName,"Chapter",chapter,"with",len(imageList),"pages")
    zip.close()



def fixResults(resultsRaw):
  fixed = []
  for result in resultsRaw:
    rList = result.get_text()
    rList = list(filter(None, rList))
    for idx, r in enumerate(rList):
      if '\xa0' in r or '\n' in r:
        rList.remove(r)
        rList[idx-1] += ' '
    s = ''.join(rList).strip()
    fixed.append( s[:50] + (s[50:]))
  return fixed



def searchForManga(search):
  pageURL = getSearchURL(search)
  request = sendRequest(pageURL)
  rawHTML = request.text
  parsedHTML = bs(rawHTML, "html.parser")
  
  resultsRaw = parsedHTML.find_all("div", {"class" : "manga_name"})
  mangaNames = fixResults(resultsRaw)
  
  resultsRaw = parsedHTML.find_all("div", {"class" : "chapter_count"})
  mangaChapters = fixResults(resultsRaw)
  for idx,chapter in enumerate(mangaChapters):
    mangaChapters[idx] = ''.join(chapter.split(" ", 1)[0]).strip()  # only get chapter count

  print("\n  Search Returned", len(mangaNames), "result(s).\n")
  for idx,r in enumerate(mangaNames):
    print("\t[" + addZeroes(str(idx), 3) + "]  " + r + " --- " + mangaChapters[idx]+ " Chapters")
  return mangaNames, mangaChapters



def inputString(prompt):
  while(True):
    try:
      x = input(prompt).title().rstrip().lstrip()
    except KeyboardInterrupt:
        endProgram("\n  Keyboard Interruption detected.")
    if not x:
      print("  Invalid input. Please retry. ")
      continue
    else:
      return x



def inputInteger(prompt, min, max):
  while(True):
    try:
      x = input(prompt).replace(" ", "")
    except KeyboardInterrupt:
        endProgram("\n  Keyboard Interruption detected.")
    try:
      x = int(x)
      if(x < min or x > max):
        print("  Index not within range [" + str(min) + ", " + str(max) + "]")
        continue
      else:
        return x
    except ValueError:
      print("  Invalid input. Please retry. ")
      continue



def endProgram(prompt = ""):
  print (prompt + "\n  Ending Program.")
  print ("  Thank you for using", PROGRAM_TITLE, "!")
  try:
    sys.exit(0)
  except SystemExit:
    os._exit(0)
  


def main(): 
  path = os.getcwd() + "/Manga/" 
  clearScreen()
  drawHeader()

  while True:
    
    search = inputString("\n\tEnter Series Name: ")
    searchResults = searchForManga(search) #tuple(mangaNames, mangaChapters)
    if len(searchResults[0]) == 0:
      clearScreen()
      drawHeader()
      print("\n  No search results found for", search, " :(")
      continue
    
    index = inputInteger("\n  Please select manga index from above: ", 0, len(searchResults[0])-1)
    seriesName = searchResults[0][index]
    totalChapters = int(searchResults[1][index])
    clearScreen()
    drawHeader()

    print("\n  Selected [" + addZeroes(str(index), 3) + "] - " + seriesName + " --- " + str(totalChapters) + " Chapters")
    chapterStart = inputInteger("\tEnter Chapter Range Start : ", 1, totalChapters)
    chapterEnd = inputInteger("\tEnter Chapter Range End : ", chapterStart, totalChapters) 
    print ("\tDownloading Chapter(s)", chapterStart, "-", chapterEnd, "\n")

    for chapter in range(chapterStart, chapterEnd + 1):
      try:
        downloadMangaChapter(seriesName, chapter, path, chapterEnd + 1) 
      except KeyboardInterrupt:
        endProgram("\n  Keyboard Interruption detected.\n  Download interrupted.\n  CBZ file was not created.")
      createCBZ(seriesName, chapter, path)
    if not yesOrNo("\n\n  Download Request Finished. Would you like to download more? "):
      break 
    else:
      clearScreen()
      drawHeader()



# Run main program loop
main()