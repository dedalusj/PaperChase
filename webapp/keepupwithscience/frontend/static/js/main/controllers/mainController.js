app.controller("mainController", function($scope, $http, $resource){
 
    $http.defaults.headers.common['Authorization'] = 'Basic ' + Base64.encode('dedalusj@gmail.com:idathik');
    
    $scope.categories = [];
    var Category = $resource('http://localhost:port/api/categories/:categoryId', {categoryId:'@id', port: ':5000'});
    
    $scope.init = function() {
        $scope.categories = Category.query(function() {
        
        });
//        var q = {order_by: [{field: "name", direction: "asc"}]};
//        $http.get('http://localhost:5000/api/categories').success(function(data, status, headers, config) {
//            As we are getting our data from an external source, we need to format the data so we can use it to our desired affect
//            For each day get all the episodes
//            angular.forEach(data.categories, function(category, index){
//                $scope.categories.push(category);
//            });
//        }).error(function(data, status, headers, config) {
//
//        });
    };
});