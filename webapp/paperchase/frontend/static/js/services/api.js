app.factory('CategoryAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource',{categoryId:'@id', resource: '@res'});
}]);

app.factory('SubscriptionAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the subscription API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/subscriptions/:journal_id',{journal_id:'@id'});
}]);

app.factory('PaperAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the paper API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/papers/:paper_id',{paper_id:'@id'});
}]);