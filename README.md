## About
This is an application I decided to make to learn more about web scraping with Python. Currently, this
will only pull from [mangareader.net](https://www.mangareader.net/). The user can specify a range of chapters to download of a specified series. The downloaded images and generated PDF will be stored in a folder named Manga in the same folder that mangascraper.exe is in.


Console Version:
![capture](https://user-images.githubusercontent.com/15623775/38115692-edb989f0-337a-11e8-8157-48410de12488.PNG)


## Development Requirements:
* **Python 3.X**    ( $ sudo apt-get install python )
* **PIP** ( $ sudo apt install python3-pip )
* **BeautifulSoup4** ( $ pip install BeautifulSoup4 )
* **Requests** ( $ pip install requests )
* **FPDF** ( $ pip install FPDF )

## How to Use:
Run **mangascraper.exe** in the **dist** folder
Downloaded manga is then stored in the /Manga directory.

## To Do:
* Create a simple frontend GUI
* Create a standalone linux executable
* Handle dynamic page sizing and orientation problems (Some pages randomly switch to landscape instead of portrait)
* Better input sanitization and confirmation of what series is being scraped
* 
