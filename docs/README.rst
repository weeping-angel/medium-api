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
        :alt: Github Actions Tests

|

.. image:: https://raw.githubusercontent.com/weeping-angel/medium-apis/main/docs/_static/MediumAPIs-Banner.png
        :align: center

|

..
        | Social Profiles:

        .. image:: https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white
                :target: https://nishu-jain.medium.com
                :alt: Author's Blog

        .. image:: https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white
                :target: https://stackoverflow.com/users/17500503/weeping-angel
                :alt: StackOverflow Profile

        | Funding

        .. image:: https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white
                :target: https://www.paypal.com/paypalme/sanskarjain1997
                :alt: Paypal Link

Python Wrapper on top of `Medium APIs (by Nishu Jain) <https://rapidapi.com/nishujain1997.19@gmail.com/api/medium2/>`_ to quickly extract data from Medium's website (https://medium.com).

Installation
------------

Install from `PyPI <https://pypi.org/project/medium-apis/>`_

.. code-block:: console

        $ pip install medium-apis

Dependency: `ujson`

| For more information, see `Detailed Installation <https://medium-apis.readthedocs.io/en/latest/installation.html>`_

Example
-------

Getting a Medium user's information and fetching his articles.

.. code-block:: python

        from medium_apis import Medium
        
        medium = Medium('YOUR_RAPIDAPI_KEY')

        user = medium.user(username="nishu-jain")

        print(f'{user.fullname} has {user.followers} followers.')

        user.fetch_articles()
        for article in user.articles:
                print(article.title)


For more examples, see `Usage <https://medium-apis.readthedocs.io/en/latest/usage.html>`_ 

How to get your RapidAPI Key
----------------------------

Steps:

        - Sign up on `RapidAPI Platform <https://rapidapi.com/auth/sign-up>`_
        - Subscribe to `Medium-APIs <https://rapidapi.com/nishujain1997.19@gmail.com/api/medium2/pricing>`_
        - Go to the API's *Endpoints* tab on the `RapidAPI Hub listing <https://rapidapi.com/nishujain1997.19@gmail.com/api/medium2/>`_ and select the API key from the **X-RapidAPI-Key** dropdown under *Header Parameters* section.

For more details, see the following links:

        - https://rapidapi.com/blog/api-glossary/api-key/
        - https://docs.rapidapi.com/docs/keys

Features
--------

Extract/Scrape/Fetch/Get:
  
    - Medium User information and user-written articles
    - Medium Articles information and their textual content 
    - Medium Publications information
    - Medium's Top Writers
    - Medium's Topfeeds (Trending, Latest, All time best, best of year/month/week)
    - Medium's LatestPosts (distributed articles)

 .. 
        Applications
        ------------

Documentation
-------------

Full Documentation at https://medium-apis.readthedocs.io

Other Materials
---------------

Medium REST APIs:

        - Swagger Documentation: https://weeping-angel.github.io/medium-apis

Related REST APIs Articles:

        - `Medium APIs - Documentation <https://medium.com/p/3384e2d08667>`_
        - `How To Retrieve Medium Stories of a User Using APIs? <https://medium.com/p/fcdb1576558a>`_
        - `Medium API: Get Posts Using Python <https://medium.com/p/e8ca4331845e>`_
        - `Medium API: Get Posts Using Node.js & Axios <https://medium.com/p/a43894efaeab>`_

Miscellaneous Articles:

        - `Best Metric to Judge a Medium Article's Popularity <https://medium.com/p/cac577609bd4>`_

License
-------

Free software: `MIT license <https://raw.githubusercontent.com/weeping-angel/medium-apis/main/LICENSE>`_

EULA: `Terms of Use <https://medium-apis.readthedocs.io/en/latest/terms_of_use.html>`_

Code of Conduct
---------------

In the interest of fostering an open and welcoming environment, all contributors, maintainers 
and users are expected to abide by the Python code of conduct: https://www.python.org/psf/codeofconduct/