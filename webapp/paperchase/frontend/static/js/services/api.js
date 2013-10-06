app.factory('CategoryAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource',{categoryId:'@id', resource: '@res'});
    
//    return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource',{},{
//        'getCategories' : { method : 'GET', isArray : true, cache : true},
//        'getSubcategories' : { method : 'GET', params: { categoryId : '@id', resource : 'subcategories' }, isArray : true, cache : true },
//        'getJournals' : { method : 'GET', params : { categoryId : '@id', resource : 'journals' }, isArray : true, cache : true }
//    });
}]);

app.factory('SubscriptionAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the subscription API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/subscriptions/:journal_id',{journal_id:'@id'});
}]);

app.factory('PaperAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the paper API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/papers/:paper_id',{},{
        'getPapers' : { method : 'GET', isArray : true, cache : true},
        'getPaper' : { method : 'GET', params: { paper_id : '@id' }, cache : true}
    });
}]);