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
    .factory('Papers', ['PaperAPI', '$http', '$injector', function (PaperAPI, $https, $injector) {

        var Papers = function (unread, since) {
            this.items = [];
            this.busy = false;
            this.page = 1;
            this.readCount = 0;
            this.selected = null;
            this.selectedId = -1;
            this.unread = unread !== 'undefined' ? unread : true;
            this.since = since;
        };

        Papers.prototype.resetPapers = function () {
            this.items = [];
            this.busy = false;
            this.page = 1;
            this.readCount = 0;
            this.selected = null;
            this.selectedId = -1;
            this.unread = true;
            this.since = undefined;
        };

        Papers.prototype.nextPage = function () {
            if (this.busy) {
                return;
            }
            this.busy = true;

            var requestParam = {page : this.page};
            if (this.unread === true) {
                requestParam.unread = true;
            }
            if (this.since !== undefined) {
                requestParam.since = this.since;
            }
            PaperAPI.getPapers(requestParam, function (papers) {
                var i, paper;
                for (i = papers.length - 1; i >= 0; i -= 1) {
                    paper = new Paper(papers[i]);
                    if (paper.read === true) {
                        this.readCount += 1;
                    }
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

            PaperAPI.getPaper({'paperId': paperId}, function (paper) {
                this.selected = new Paper(paper);
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

        Papers.prototype.showAll = function () {
            this.resetPapers();
            this.unread = false;
            this.nextPage();
        };

        Papers.prototype.showUnread = function () {
            this.resetPapers();
            this.unread = true;
            this.nextPage();
        };

        Papers.prototype.markAllRead = function () {
            PaperAPI.markAllRead();
        };
        return Papers;
    }]);