PaperChase
==========

PaperChase is an RSS reader aimed at people working in academia. 

One of the main tasks of an academic is to keep up with new pubblications and research. With an ever increasing number of journals and articles published every day filtering interesting work becomes difficult.

PaperChase uses RSS feeds published by pubblications to detect when new articles are published. It then connects to the journal website to extract information, e.g. abstracts, that wasn't available in the feed but that it is still available for free to unregistered users.

It aims at ranking every new article according to the user research interests making it easier to stay on top of new developments in your field.

It serves the articles it collects through vartious medium, web, mobile and desktop application in order to maximise its reach and usefulness to the community.

Details
-------

The core of the project is a backend server built using the [Flask](http://flask.pocoo.org/) microframework for Python and serving a REST-like API for clients to connect to.

PaperChase uses [Celery](http://www.celeryproject.org/) to run background tasks that 
* grab new articles from the RSS feeds
* extract missing informations from their webpages
* insert them into the database

The extraction of missing information from the article's webpage is accomplished using XPath making the process easily extensible to different websites and different kind of information.
The web app, and the other clients later, implements an easy interface to let users suggest new journals and the paths of the information to extract.

Every access to the API requires HTTP Basic authentication and the backend implement user registration and verification using [Flask-Security](http://pythonhosted.org/Flask-Security/).

The web client is implemented using [AngularJS](http://angularjs.org/) that serves all the views of the app.

Requirements
------------

* Mac OS X
* Python 2.7
* MySQL 5.6.12
* Redis

Status
------

### Implemented

#### Backend

* Part of the database that stores articles, journals and categories for the journal.
* Background workers for the parsing of RSS feeds and saving of new articles.
* User registration and security of the API reuqests.
* API for the submission of new journal suggestions.
* API for the exploration of categories, journals and subscriptions.

#### Frontend

* Main AngularJS app module.
* Login view and store of the user security credentials.
* Resource service for the categories and journals.
* Categories and Journals view.
* Journal suggestion view.

### TODO

#### Backend

* Storage of read/unread articles for every user.
* Storage of article score for every user.
* API for serving articles and setting articles attributes: read/unread, score, etc.
* Storage of user keywords.
* API for serving keywords and their relevance for each user.

The backend API is still rapidly evolving and as such is currently undocumented. Once the APIs for the keywords and articles are implemented I'll work on the documentation for clients. 

#### Frontend

* Resource for keywords and their retrieval.
* Resource for articles and their retrieval.
* Scoring of articles locally.
* Setting articles attributes (read/unread, scores, etc.) on the backend through API post requests.
* Keywords tuning view.
* Main view with articles.
