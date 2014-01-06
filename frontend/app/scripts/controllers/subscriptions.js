/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .controller('SubscriptionsCtrl', ['$scope', 'Journals', 'CategoryAPI', function ($scope, Journals, CategoryAPI) {
        
        $scope.journals = new Journals();
        // Start by grabbing the list of journals
        $scope.journals.getJournals();
        
        $scope.categories = CategoryAPI.getCategories();
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

        $scope.resetSubcategory = function () {
            $scope.subcategory = {name: 'All', id: undefined};
        };
        $scope.resetSubcategory();

        $scope.selectCategory = function (cat) {
            $scope.category = cat;
            $scope.resetSubcategory();
        };

        $scope.resetCategory = function () {
            $scope.category = {name: 'All', id: undefined, subcategories: []};
            $scope.resetSubcategory();
        };
        $scope.resetCategory();

        $scope.subscribe = function ($event, journalId) {
            $scope.journals.toggleSubscriptions(journalId, true);
        };
        $scope.unsubscribe = function ($event, journalId) {
            $scope.journals.toggleSubscriptions(journalId, false);
        };
    }]);