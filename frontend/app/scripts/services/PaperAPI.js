/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('PaperAPI', ['$http', '$resource', function ($http, $resource) {
        // Define the resource for the paper API to be shared by all other services and controllers
        return $resource('/api/papers/:paper_id', {}, {
            'getPapers' : { method : 'GET', isArray : true},
            'getPaper' : { method : 'GET', params: { paper_id : '@id' }},
            'getUnreadList' : { url : '/api/unread_papers', method : 'GET', isArray : true},
            'markUnread' : { url : '/api/unread_papers', method : 'PUT', isArray : true },
            'markRead' : { url : '/api/read_papers', method : 'PUT', isArray : true },
            'markAllRead' : { url : '/api/read_papers/mark_all_read', method : 'PUT'}
        });
    }]);