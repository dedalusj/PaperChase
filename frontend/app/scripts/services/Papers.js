/*jslint browser: true */
'use strict';

function Paper(paper) {
    this.selected = false;
    angular.extend(this, paper);
    this.init();
}

Paper.prototype.init = function () {
    this.created = new Date(this.created);
    this.read = this.readAt !== null;
};

angular.module('paperchaseApp')
    .factory('Papers', ['PaperAPI', 'Journals', '$injector', '$q', function (PaperAPI, Journals, $injector, $q) {

        var journals = Journals;

        // var Papers = function (unread, since) {
        var Papers = function (unread, since, journalId) {
            this.items = [];
            this.busy = false;
            this.readCount = 0;
            this.selected = null;
            this.selectedId = -1;
            this.page = 1;

            // we set the number of pages to 1 because we always assume to be at least a page
            // if simply there are no results we would get a 404 error that is ingored by the browser
            this.numberOfPages = 1;

            var _since = since;
            this.__defineGetter__('since', function () {
                return _since;
            });

            // true is the default for a new Papers object
            var _unread = unread !== undefined ? unread : true;
            this.__defineGetter__('unread', function (){
                return _unread;
            });

            var _journalId = journalId;
            this.__defineGetter__('journalFilter', function () {
                return _journalId;
            });
        };

        Papers.prototype.nextPage = function () {
            // return if we are already retrieving stuff or we fetched the last page already
            if (this.busy || (this.page > this.numberOfPages)) {
                return;
            }
            this.busy = true;

            // Compose the dictionary with the request parameters
            var requestParam = {page : this.page};
            if (this.unread === true) {
                requestParam.unread = true;
            }
            if (this.since !== undefined) {
                requestParam.since = this.since;
            }

            var subscriptions = journals.subscriptions,
                papers;
            if (this.journalFilter === undefined) {
                papers = PaperAPI.getPapers(requestParam, function(data, headers) {
                    this.numberOfPages = headers()['x-total-count'];
                }.bind(this));
            } else {
                requestParam.journalId = this.journalFilter;
                papers = PaperAPI.getPapersForJournal(requestParam, function(data, headers) {
                    this.numberOfPages = headers()['x-total-count'];
                }.bind(this));
            }
            
            $q.all([
                papers.$promise,
                subscriptions.$promise
            ]).then(function() {
                var i, paper;
                for (i = papers.length - 1; i >= 0; i -= 1) {
                    paper = new Paper(papers[i]);
                    if (paper.read === true) {
                        this.readCount += 1;
                    }
                    paper.journal = journals.findSubscription(paper.journalId);
                    delete paper.journalId;
                    this.items.push(paper);
                }
                this.page = this.page + 1;
                this.busy = false;
            }.bind(this));
        };

        Papers.prototype.hasPrev = function () {
            if (!this.selected) {
                return true;
            }
            return this.selectedId > 0;
        };

        Papers.prototype.hasNext = function () {
            if (!this.selected) {
                return true;
            }
            return this.selectedId < this.items.length - 1;
        };

        Papers.prototype.selectItem = function (paperId) {
            var i = 0,
                rootScope = $injector.get('$rootScope');

            var paper = PaperAPI.getPaper({'paperId': paperId});
            var subscriptions = journals.subscriptions;
            $q.all([
                paper.$promise,
                subscriptions.$promise
            ]).then(function() {
                this.selected = new Paper(paper);
                this.selected.journal = journals.findSubscription(this.selected.journalId);
                delete this.selected.journalId;
                if (!this.selected.read) {
                    this.toggleRead();
                }
            }.bind(this));

            // Unselect previous selection.
            if (this.selectedId >= 0) {
                this.items[this.selectedId].selected = false;
            }
            while (i < this.items.length) {
                if (this.items[i].id === paperId) {
                    this.selectedId = i;
                    break;
                }
                i += 1;
            }
            this.items[this.selectedId].selected = true;
            if (rootScope) {
                rootScope.$broadcast('selected_new_item', paperId);
            }
            if (!this.hasNext()) {
                this.nextPage();
            }
        };

        Papers.prototype.prev = function () {
            if (this.hasPrev()) {
                this.selectItem(this.items[this.selected ? this.selectedId - 1 : 0].id);
            }
        };

        Papers.prototype.next = function () {
            if (this.hasNext()) {
                this.selectItem(this.items[this.selected ? this.selectedId + 1 : 0].id);
            }
        };

        Papers.prototype.toggleRead = function () {
            if (this.selected.read === false) {
                PaperAPI.markRead({ readPapers : [this.selected.id] });
            } else {
                PaperAPI.markUnread({ unreadPapers : [this.selected.id] });
            }
            this.selected.read = !this.selected.read;
            this.items[this.selectedId].read = !this.items[this.selectedId].read;
        };

        Papers.prototype.markAllRead = function () {
            PaperAPI.markAllRead();
        };

        return Papers;
    }]);