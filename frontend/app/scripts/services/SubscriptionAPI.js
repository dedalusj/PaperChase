/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('SubscriptionAPI', ['$http', '$resource', function ($http, $resource) {

        return $resource('/api/subscriptions/:journalId', {}, {
            'getSubscribedJournals' : { method : 'GET', isArray : true},
            'subscribe' : { method : 'POST', params : { journalId : '@id' }},
            'unsubscribe' : { method : 'DELETE', params : { journalId : '@id' }}
        });

    }]);