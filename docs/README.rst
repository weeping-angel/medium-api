..
        Readme page for github and PyPI

===========
Medium APIs
===========

.. image:: https://img.shields.io/pypi/v/medium-apis
        :target: https://pypi.python.org/pypi/medium_apis
        :alt: PYPI Package Version

.. image:: https://readthedocs.org/projects/medium-apis/badge/?version=latest
        :target: https://medium-apis.readthedocs.io/en/latest/?version=latest
        :alt: RTD Documentation Status

.. image:: https://github.com/weeping-angel/medium-apis/actions/workflows/tests.yml/badge.svg

.. raw:: html

        <div align="center">
        <img src="_static/MediumAPIs-Banner.png" />
        </div><br/>

..
        | Social Profiles:

        .. image:: https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white
                :target: https://user-jain.medium.com
                :alt: Author's Blog

        .. image:: https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white
                :target: https://stackoverflow.com/users/17500503/weeping-angel
                :alt: StackOverflow Profile

        | Funding

        .. image:: https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white
                :target: https://www.paypal.com/paypalme/sanskarjain1997
                :alt: Paypal Link

Python Wrapper on top of `Medium API <https://rapidapi.com/userjain1997.19@gmail.com/api/medium2/>`_ to quickly extract data from Medium's website (https://medium.com).

Installation
------------

Install from `PyPI <https://pypi.org/project/medium-apis/>`_

.. code-block:: console

        $ pip install medium-apis

Dependency: ``ujson``

Usage
-----

Getting a Medium user's information and fetching his articles.

.. code-block:: python

        from medium_apis import Medium
        
        medium = Medium('YOUR_RAPIDAPI_KEY')

        user = medium.user(username="nishu-jain")

        print(f'{user.fullname} has {user.followers} followers.')

        user.fetch_articles()
        for article in user.articles:
                print(article.title)


How to get your RapidAPI Key
----------------------------


Documentation
-------------

Full Documentation at https://medium-apis.readthedocs.io


Features
--------

Extract/Scrape/Fetch/Get :
  
    * Medium User information and user-written articles
    * Medium Articles information and their textual content 
    * Medium Publications information
    * Medium's Top Writers
    * Medium's Topfeeds (Trending, Latest, All time best, best of year/month/week)
    * Medium's LatestPosts (distributed articles)
    * And so on ...
  
Applications
------------

Other Materials
---------------

Medium REST APIs:

        - Swagger Documentation: https://weeping-angel.github.io/medium-apis

License
-------

Free software: `MIT license <https://raw.githubusercontent.com/weeping-angel/medium-apis/main/LICENSE>`_

Code of Conduct
---------------

In the interest of fostering an open and welcoming environment, all contributors, maintainers 
and users are expected to abide by the Python code of conduct: https://www.python.org/psf/codeofconduct/