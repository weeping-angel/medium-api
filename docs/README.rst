..
        Readme page for github and PyPI

===========
Medium APIs
===========

.. raw:: html

        <div align="center">
        <a href="https://pypi.python.org/pypi/medium_apis"><img alt="PYPI Package Version" src="https://img.shields.io/pypi/v/medium-apis" /></a>
        <a href="https://medium-apis.readthedocs.io/en/latest/?version=latest"><img alt="RTD Documentation Status" src="https://readthedocs.org/projects/medium-apis/badge/?version=latest" /></a>
        <img alt="Github Actions Tests" src="https://github.com/weeping-angel/medium-apis/actions/workflows/tests.yml/badge.svg" />
        </div>
        <br/>
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

Python Wrapper on top of `Medium APIs (by Nishu Jain) <https://rapidapi.com/nishujain1997.19@gmail.com/api/medium2/>`_ to quickly extract data from Medium's website (https://medium.com).

Installation
------------

Install from `PyPI <https://pypi.org/project/medium-apis/>`_

.. code-block:: console

        $ pip install medium-apis

Dependency: ``ujson``

| For more detailed installation, see `Installation <https://medium-apis.readthedocs.io/en/latest/installation.html>`_

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

Documentation
-------------

Full Documentation at https://medium-apis.readthedocs.io

Other Materials
---------------

Medium REST APIs:

        - Swagger Documentation: https://weeping-angel.github.io/medium-apis

License
-------

Free software: `MIT license <https://raw.githubusercontent.com/weeping-angel/medium-apis/main/LICENSE>`_

Terms of Use
------------



Code of Conduct
---------------

In the interest of fostering an open and welcoming environment, all contributors, maintainers 
and users are expected to abide by the Python code of conduct: https://www.python.org/psf/codeofconduct/