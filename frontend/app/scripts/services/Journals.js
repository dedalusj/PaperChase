/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('Journals', ['SubscriptionAPI', 'JournalAPI', '$modal', '$location', function (SubscriptionAPI, JournalAPI, $modal, $location) {
        
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

        // Called when the number of subscriptions is zero
        // If we are not on the subscriptions page already show a modal dialog
        // and redirect the user to the subscription page
        var emptySubscriptions = function () {
            if ($location.path() !== '/subscriptions') {
                var modalInstance = $modal.open({
                    templateUrl: 'views/emptysubdialog.html',
                    controller: 'ModalCtrl',
                    resolve: {}
                });
                modalInstance.result.then(function () {
                    $location.path('/subscriptions');
                });
            }
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
                return SubscriptionAPI.getSubscribedJournals(function(data) {
                    // Don't show the no subscription dialog if we are already on the page
                    if (data.length === 0) {
                        emptySubscriptions();
                    }
                });
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
            // find the journal we are about to update
            var journal = this.findJournal(journalId);

            // hit the subscription API endpoint and update the journal subscribe
            // property when the response comes back
            if (subscribe === true) {
                SubscriptionAPI.subscribe({'journalId': journalId}, function (data) {
                    journal.subscribed = data.subscribed;
                });
            } else {
                SubscriptionAPI.unsubscribe({'journalId': journalId}, function (data) {
                    journal.subscribed = data.subscribed;
                });
            }

            // finally refresh the subscriptions list since we change the state of a journal
            this.refreshSubscriptions();
        };

        return new Journals();
    }]);
