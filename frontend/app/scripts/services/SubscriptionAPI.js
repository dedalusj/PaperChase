/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('SubscriptionAPI', ['$http', '$resource', function ($http, $resource) {
        // Define the resource for the subscription API to be shared by all other services and controllers
        return $resource('/api/subscriptions/:journal_id', {journal_id : '@id'});
    }]);