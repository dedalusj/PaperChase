app.factory('CategoryAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/categories/:categoryId/:resource',{categoryId:'@id', resource: '@res'});
}]);

app.factory('SubscriptionAPI', ['$http', '$resource', function($http, $resource) {
    // Define the resource for the category API to be shared by all other services and controllers
    return $resource('http://localhost\\:5000/api/subscriptions/:journal_id',{journal_id:'@id'});
}]);