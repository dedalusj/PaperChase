PaperChase
==========

PaperChase is an RSS reader aimed at people working in academia. 

One of the main tasks of an academic is to keep up with new publications and research. With an ever increasing number of journals and articles published every day filtering interesting work becomes difficult.

PaperChase uses RSS feeds published by publications to detect when new articles are published. It then connects to the journal website to extract information, e.g. abstracts, that wasn't available in the feed but that it is still available for free to unregistered users.

It aims at ranking every new article according to the user research interests making it easier to stay on top of new developments in your field.

It serves the articles it collects through various medium, web, mobile and desktop application in order to maximise its reach and usefulness to the community.

Details
-------

The core of the project is a backend server built using the [Flask](http://flask.pocoo.org/) micro-framework for Python and serving a REST-like API for clients to connect to.

PaperChase uses [Celery](http://www.celeryproject.org/) to run background tasks that 
* grab new articles from the RSS feeds
* extract missing information from their webpages
* insert them into the database

The extraction of missing information from the article's webpage is accomplished using XPath making the process easily extensible to different websites and different kind of information.
The web app, and the other clients later, implements an easy interface to let users suggest new journals and the paths of the information to extract.

Every access to the API requires HTTP Basic authentication.

The web client is implemented using [AngularJS](http://angularjs.org/) that serves all the views of the app.

The aesthetics of Paperchase is currently inspired by [Feedbin](https://feedbin.me/) by [Ben Ubois](https://github.com/benubois). 

Installation and requirements
-----------------------------

* Mac OS X or Linux
* Python 2.7
* MySQL 5.6.12
* Redis

### Install

- [Mac OS X](webapp/docs/OS%20X%20Setup.md)

TODO
----

### Backend

* Storage of article score for every user.
* Storage of user keywords.
* API for serving keywords and their relevance for each user.

The backend API is still rapidly evolving and as such is currently undocumented. Once the APIs for the keywords and articles are implemented I'll work on the documentation for clients. 

### Frontend

* Resource for keywords and their retrieval.
* Scoring of articles locally.
* Keywords tuning view.

### Other Clients

* iOS client
* Mac OS X client
* Mobile

License
-------

Paperchase is available under the MIT license. See the LICENSE file for more info.
