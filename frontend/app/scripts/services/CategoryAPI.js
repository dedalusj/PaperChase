/*jslint browser: true */
'use strict';

angular.module('paperchaseApp')
    .factory('CategoryAPI', ['$http', '$resource', function ($http, $resource) {
        return $resource('/api/categories/:category_id/:resource', {}, {
            'getCategories' : { method : 'GET', isArray : true, cache : true},
            'getSubcategories' : { method : 'GET', params: { category_id : '@id', resource : 'subcategories' }, isArray : true, cache : true },
            'getJournals' : { method : 'GET', params : { category_id : '@id', resource : 'journals' }, isArray : true, cache : true }
        });
    }]);