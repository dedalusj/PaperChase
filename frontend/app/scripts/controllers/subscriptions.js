/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .controller('SubscriptionsCtrl', ['$scope', 'CategoryAPI', 'SubscriptionAPI', 'JournalAPI', function ($scope, CategoryAPI, SubscriptionAPI, JournalAPI) {
        
        $scope.categories = CategoryAPI.getCategories();
        $scope.journals = JournalAPI.getJournalsWithSubscriptions();
        
        $scope.subscribed = {name: 'All', value: undefined};
        $scope.subscriptionFilter = function (status) {
            $scope.subscribed.value = status;
            switch(status)
            {
            case true:
                $scope.subscribed.name = 'Subscribed';
                break;
            case false:
                $scope.subscribed.name = 'Unsubscribed';
                break;
            default:
                $scope.subscribed.name = 'All';
            }
        };

        $scope.resetCategory = function () {
            $scope.category = {name: 'All', id: undefined, subcategories: []};
        };
        $scope.resetCategory();

        $scope.subscribe = function ($event, journalId) {
            var newSubscription = new SubscriptionAPI({'journalId': journalId}),
                journal = $scope.findJournal(journalId);
            newSubscription.$save();
            if (journal) {
                journal.subscribed = true;
            }
        };
        $scope.unsubscribe = function ($event, journalId) {
            SubscriptionAPI.remove({'journalId': journalId});
            var journal = $scope.findJournal(journalId);
            if (journal) {
                journal.subscribed = false;
            }
        };
        $scope.findJournal = function (journalId) {
            var i = 0, journal;
            while (i < $scope.journals.length) {
                if ($scope.journals[i].id === journalId) {
                    journal = $scope.journals[i];
                    break;
                }
                i += 1;
            }
            return journal;
        };
    }]);