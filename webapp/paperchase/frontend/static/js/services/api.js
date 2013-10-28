app.factory('CategoryAPI', ['$http', '$resource', function($http, $resource) {
    return $resource('/api/categories/:category_id/:resource',{},{
        'getCategories' : { method : 'GET', isArray : true, cache : true},
        'getSubcategories' : { method : 'GET', params: { category_id : '@id', resource : 'subcategories' }, isArray : true, cache : true },
        'getJournals' : { method : 'GET', params : { category_id : '@id', resource : 'journals' }, isArray : true, cache : true }
    });
}]);

app.factory('SubscriptionAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the subscription API to be shared by all other services and controllers
    return $resource('/api/subscriptions/:journal_id',{journal_id : '@id'});
}]);

app.factory('PaperAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the paper API to be shared by all other services and controllers
    return $resource('/api/papers/:paper_id',{},{
        'getPapers' : { method : 'GET', isArray : true},
        'getPaper' : { method : 'GET', params: { paper_id : '@id' }},
        'getUnreadList' : { url : '/api/unread_papers', method : 'GET', isArray : true},
        'markUnread' : { url : '/api/unread_papers', method : 'PUT', isArray : true },
        'markRead' : { url : '/api/read_papers', method : 'PUT', isArray : true },
        'markAllRead' : { url : '/api/read_papers/mark_all_read', method : 'PUT'}
    });
}]);