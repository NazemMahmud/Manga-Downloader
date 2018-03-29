## About
This is an application I decided to make to learn more about web scraping with Python. Currently, this
will only pull from [mangareader.net](https://www.mangareader.net/). The user can specify a range of chapters to download of a specified series. The downloaded images will be stored in the same folder that mangascraper.py is located.


Console Version:
![capture](https://user-images.githubusercontent.com/15623775/38115692-edb989f0-337a-11e8-8157-48410de12488.PNG)


## Requirements:
* **Python 3.X**    ( $ sudo apt-get install python )
* **PIP** ( $ sudo apt install python3-pip )
* **BeautifulSoup4** ( $ pip install BeautifulSoup4 )
* **Requests** ( $ pip install requests )

## How to Use:
Navigate to directory containing mangascraper.py in terminal. Then, run
```
$ python mangascraper.py
```


## To Do:
* Option to convert all retrieved images to a single pdf or mobi file
* Create a simple frontend GUI
* Create a standalone windows and linux executable using pyinstaller/py2exe
