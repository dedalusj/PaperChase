'use strict';

angular.module('paperchaseApp')
    .service('JournalAPI', ['$http', '$resource', function Journalapi($http, $resource) {
        return $resource('/api/journals/:journalId', {}, {
            'getJournals' : { method : 'GET', isArray : true, cache : true},
            'getJournal' : { method : 'GET', params: { journalId : '@id' }, isArray : false, cache : true }
        });
    }]);
