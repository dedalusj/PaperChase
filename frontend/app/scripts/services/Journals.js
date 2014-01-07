/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('Journals', ['SubscriptionAPI', 'JournalAPI', function (SubscriptionAPI, JournalAPI) {
        
        var findJournal = function (journalId, journalsArray) {
            var i = 0, journal;
            while (i < journalsArray.length) {
                if (journalsArray[i].id === journalId) {
                    journal = journalsArray[i];
                    break;
                }
                i += 1;
            }
            return journal;
        };

        var Journals = function () {
            this.journals = [];

            var getSubscriptions = function () {
                // We use this subscription list to display the data for the journals in the main page
                // we are going to hit this array every time we display a paper hence it needs to
                // be quickly searchable and we are going to use binary search so we sort it
                // http://oli.me.uk/2013/06/08/searching-javascript-arrays-with-a-binary-search/

                // this.subscriptions.sort(function (a, b) {
                //     return a.id < b.id ? -1 : 1;
                // });
                return SubscriptionAPI.getSubscribedJournals();
            };

            this.__defineGetter__('subscriptions', function(){
                if (this._subscriptions === undefined) {
                    this._subscriptions = getSubscriptions();
                }
                return this._subscriptions;
            });

            this.refreshSubscriptions = function ()  {
                // the subscriptions property caches its value for performance
                // we need this method to force a refresh when needed
                this._subscriptions = getSubscriptions();
            };
   
        };

        Journals.prototype.getJournals = function () {
            this.journals = JournalAPI.getJournals();
        };

        Journals.prototype.findJournal = function (journalId) {
            return findJournal(journalId, this.journals);
        };

        Journals.prototype.findSubscription = function (journalId) {
            return findJournal(journalId, this._subscriptions);
        };

        Journals.prototype.toggleSubscriptions = function (journalId, subscribe) {
            // hit the subscription API endpoint
            if (subscribe === true) {
                SubscriptionAPI.subscribe({'journalId': journalId});
            } else {
                SubscriptionAPI.unsubscribe({'journalId': journalId});
            }

            // update the list of journals we keep in memory
            var journal = this.findJournal(journalId);
            if (journal) {
                journal.subscribed = subscribe;
            }

            // if we grabbed the list of subscriptions before we need to refresh it
            if (this._subscriptions !== undefined) {
                this.refreshSubscriptions();
            }
        };

        return new Journals();
    }]);
