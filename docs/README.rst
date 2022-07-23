..
        Readme page for github and PyPI

===========
Medium API
===========

.. image:: https://img.shields.io/pypi/v/medium-api?label=PyPI
        :target: https://pypi.python.org/pypi/medium_api
        :alt: PYPI Package Version

.. image:: https://img.shields.io/pypi/dm/medium-api?color=darkgreen&label=Downloads
        :target: https://pypistats.org/packages/medium-api
        :alt: PYPI Monthly Download Stats

.. image:: https://readthedocs.org/projects/medium-api/badge/?version=latest
        :target: https://medium-api.readthedocs.io/en/latest/?version=latest
        :alt: RTD Documentation Status

.. image:: https://github.com/weeping-angel/medium-api/actions/workflows/tests.yml/badge.svg
        :alt: Github Actions Tests

|

.. image:: https://raw.githubusercontent.com/weeping-angel/medium-api/main/docs/_static/MediumAPI-GettingStarted-Thumbnail.png
        :target: https://www.youtube.com/watch?v=oc8TKG9EQfE
        :alt: What is Medium API?
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

Python Wrapper on top of `Medium API (by Nishu Jain) <http://hub.mediumapi.com>`_ to quickly extract data from Medium's website (https://medium.com).

Installation
------------

Install from `PyPI <https://pypi.org/project/medium-api/>`_

.. code-block:: console

        $ pip install medium-api

Dependency: `ujson`

| For more information, see `Detailed Installation <https://medium-api.readthedocs.io/en/latest/installation.html>`_

Example
-------

Getting a Medium user's information and fetching his articles.

.. code-block:: python

        from medium_api import Medium
        
        medium = Medium('YOUR_RAPIDAPI_KEY')

        user = medium.user(username="nishu-jain")

        print(f'{user.fullname} has {user.followers_count} followers.')

        user.fetch_articles()
        for article in user.articles:
                print(article.title)


For more examples, see `Usage <https://medium-api.readthedocs.io/en/latest/usage.html>`_ 

How to get your RapidAPI Key
----------------------------

.. image:: https://img.youtube.com/vi/-MM1C6mb-mc/0.jpg
        :align: center
        :target: https://www.youtube.com/watch?v=-MM1C6mb-mc
        :alt: How to get your RapidAPI Key (Subscribe to Medium API)

Steps:

        - Sign up on `RapidAPI Platform <https://rapidapi.com/auth/sign-up>`_
        - Subscribe to `Medium-API <http://hub.mediumapi.com/pricing>`_
        - Go to the API's *Endpoints* tab on the `RapidAPI Hub listing <http://hub.mediumapi.com>`_ and select the API key from the **X-RapidAPI-Key** dropdown under *Header Parameters* section.

For more details, see the following links:

        - https://rapidapi.com/blog/api-glossary/api-key/
        - https://docs.rapidapi.com/docs/keys

Features
--------

Extract/Scrape/Fetch/Get:
  
    - Medium User information and User-written Articles
    - Medium User's Followers and Following
    - Medium Articles information
    - Medium Article's Textual Content and Markdown
    - Medium Article's Responses/Comments 
    - Medium Publications information
    - Medium Publication's Articles
    - Medium's Top Writers
    - Medium's Topfeeds (Trending, Latest, All time best, best of year/month/week)
    - Medium's LatestPosts (distributed articles)

 .. 
        Applications
        ------------

Documentation
-------------

Full Documentation at https://medium-api.readthedocs.io

Other Materials
---------------

Medium REST API:

        - Swagger Documentation: https://weeping-angel.github.io/medium-api

Related REST API Articles:

        - `Medium API - Documentation <https://medium.com/p/3384e2d08667>`_
        - `How To Retrieve Medium Stories of a User Using API? <https://medium.com/p/fcdb1576558a>`_
        - `Medium API: Get Posts Using Python <https://medium.com/p/e8ca4331845e>`_
        - `Medium API: Get Posts Using Node.js & Axios <https://medium.com/p/a43894efaeab>`_

Miscellaneous Articles:

        - `Best Metric to Judge a Medium Article's Popularity <https://medium.com/p/cac577609bd4>`_
        - `How To Leverage Medium for Crypto-trading <https://medium.com/p/deedea890da1>`

License
-------

Free software: `MIT license <https://raw.githubusercontent.com/weeping-angel/medium-api/main/LICENSE>`_

EULA: `Terms of Use <https://medium-api.readthedocs.io/en/latest/terms_of_use.html>`_

Code of Conduct
---------------

In the interest of fostering an open and welcoming environment, all contributors, maintainers 
and users are expected to abide by the Python code of conduct: https://www.python.org/psf/codeofconduct/