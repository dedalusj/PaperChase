app.factory('CategoryAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
//    return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource',{categoryId:'@id', resource: '@res'});
    
    return $resource('http://localhost\\:5000/api/categories/:category_id/:resource',{},{
        'getCategories' : { method : 'GET', isArray : true, cache : true},
        'getSubcategories' : { method : 'GET', params: { category_id : '@id', resource : 'subcategories' }, isArray : true, cache : true },
        'getJournals' : { method : 'GET', params : { category_id : '@id', resource : 'journals' }, isArray : true, cache : true }
    });
}]);

app.factory('SubscriptionAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the subscription API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/subscriptions/:journal_id',{journal_id : '@id'});
}]);

app.factory('PaperAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the paper API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/papers/:paper_id',{},{
        'getPapers' : { method : 'GET', isArray : true},
        'getPaper' : { method : 'GET', params: { paper_id : '@id' }},
        'getUnreadList' : { url : 'http://localhost\\:5000/api/unread_papers', method : 'GET', isArray : true},
        'markUnread' : { url : 'http://localhost\\:5000/api/unread_papers', method : 'PUT', isArray : true },
        'markRead' : { url : 'http://localhost\\:5000/api/read_papers', method : 'PUT', isArray : true },
        'markAllRead' : { url : 'http://localhost\\:5000/api/read_papers/mark_all_read', method : 'PUT'}
    });
}]);