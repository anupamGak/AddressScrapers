Nissan
======

Introduction
------------

Scraps address of dealers of Nissan in India [Nissan Find a Dealer](https://www.nissan.in/find-a-dealer.html).
The data, including _lat_ and _long_, was found in [this](https://www.nissan.in/content/nissan/en_IN/index/find-a-dealer/jcr:content/freeEditorial/columns12/col1-par/find_a_dealer.extended_dealers_by_location.json?_charset_=utf-8&page=1&size=179) URL present in Nissan's domain.

Dependencies
------------

The scrawler depends on ``lxml``.
As the site requires SNI support which is unavailable by default in Python 2, the following _must_ be installed:


*[pyOpenSSL](https://pypi.python.org/pypi/pyOpenSSL)
* [ndg-httpsclient](https://pypi.python.org/pypi/ndg-httpsclient)
* [pyasn1](https://pypi.python.org/pypi/pyasn1/)

Usage
-----

```sh
$ python iocl_spider.py
```

Author
------

Anupam
