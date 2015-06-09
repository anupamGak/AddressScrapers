Nike
====

Introduction
------------

Scraps address of showrooms from the webpage [Nike Store Locator](http://www.nike.com/in/en_gb/sl/store-locator).
The data is obtained by passing _lat_,_long_ as parameters to this [URL](http://www.nike.com/store-locator/locations) which returns `JSON` objects.

The __lat__ and __long__ values for the showrooms are provided by the website itself.

Dependencies
------------

The scrawler depends on ``lxml``.

Usage
-----

```sh
$ python nike_spider.py
```

Author
------

Anupam