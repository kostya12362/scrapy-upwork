# scrapy-upwork

## Installation
first install the virtual environment
```bash
$ pip install virtualenv
```

The next step is to create a directory in which our folder will be in the environment
```linux
$ mkdir scrapy_spider && cd scrapy_spider
$ python3 -m venv venv
```
We activate the environment
```linux
$ source venv/bin/activate
```
We create a project
```linux
$ scrapy startproject news
$ cd news
```
```linux
$ scrapy genspider news112 112.ua
$ cd news/spiders
$ git clone https://github.com/kostya12362/scrapy-upwork.git
$ cd /scrapy-upwork
```
## Fix settings
In your settings.py file comment out
```python
#ROBOTS TXT OBEY = True
```
## Run spider 
To start and save the file in csv, run
```linux
$ scrapy crawl grec -o full.csv
```
