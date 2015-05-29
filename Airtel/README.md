Airtel website crawler
======================

Introduction
------------

The link for the webpage is [Airtel Store Locator](http://www.airtel.in/personal/internet/4g/store-locator?&utm_source=airtel_4g_dr_google_search&utm_medium=cpc&utm_lp=4g_new_url&utm_content=selected_location_ad&utm_campaign=srch%20-%20dsa&cid=ps)

Dependencies
------------

The scrawler depends on [scrapy](http://scrapy.org/),which needs to be installed. The doumentation for the same is at [scrapy docs](http://doc.scrapy.org/en/latest/intro/tutorial.html).

Usage
-----

Change directory to /src/address and run the following:
```sh
$ scrapy crawl addr
```
To get output in a .json file :
 ```sh
$ scrapy crawl addr -o <filename>.json
```

Author
------

Anupam